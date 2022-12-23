import pymysql
from sns_basics import publish_message_to_sns
import os
import json

class NimbusResource:
    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        # user = os.environ.get("DBUSER")
        # pw = os.environ.get("DBPW")
        # host = os.environ.get("DBHOST")

        user = "admin"
        password = "dbpassword"
        host = "nimbus-db.c4dwsoa8ic0w.us-east-1.rds.amazonaws.com"

        conn = pymysql.connect(
            user=user,
            password=password,
            host=host,
            port=3306,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn
    # Helper Methods for creating SQL statements for specific SQL types

    @staticmethod
    def _get_table_schema(table):
        conn = NimbusResource._get_connection()
        sql = f"DESCRIBE event.{table}"
        cur = conn.cursor()
        cur.execute(sql)

        # Fetch and print the meta-data of the table
        result = cur.fetchall()
        col_name_to_type = {}
        for col in result:
            col_name_to_type[col['Field']] = col['Type']
        return col_name_to_type

    @staticmethod
    def _create_stmt_from_type(col_type, stmt):
        if col_type == 'time':
            return f"time('{stmt}')"
        elif col_type == 'int':
            return stmt
        elif col_type == 'date':
            return f"date('{stmt}')"
        elif 'varchar' in col_type:
            stmt_escaped = stmt.replace("'", "\\\'")
            return f"'{stmt_escaped}'"

    @ staticmethod
    def get_events():
        """ Gets all events in event.event
            Returns: all events
        """
        sql = "SELECT * FROM event.event"
        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()

        return result

    @ staticmethod
    def get_event_info(event_id):
        """Returns from event.event join event.attendees
            Params: event_id
            Returns: event information and ticket information
        """
        sql = f"""
        select * FROM event.event e left join event.location l
         on e.event_id = l.event_id where e.event_id={event_id};
        """
        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()

        return result

    @ staticmethod
    def get_event_attendees(event_id):
        """Gets event information & ticket information
            Params: event_id
            Returns: attendee information
        """
        sql = f"""
            select * from
             event.attendees
                 join attendee.contact_info
                     on attendees.attendee_id = contact_info.attendee_id
            where event_id='{event_id}'"""
        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()

        return result
    
    @ staticmethod
    def get_event_attendees_emails(event_id):
        """Gets event attendee emails
            Params: event_id
            Returns: attendee emails
        """
        sql = f"""
            select email_address from
             event.attendees
                 join attendee.contact_info
                     on attendees.attendee_id = contact_info.attendee_id
            where event_id='{event_id}'"""
        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()

        return result

    @ staticmethod
    def get_organizer_events(organizer_id):
        """Gets event information & ticket information for an organizer
            Params: organizer_id
            Returns: event information
        """
        sql = f"""
            select * from
                event.event
                where organizer_id='{organizer_id}'"""
        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()

        return result

    @ staticmethod
    def get_users_events(attendee_id):
        """Gets event information & ticket information for a user
            Params: attendee_id
            Returns: event information
        """
        sql = f"""
            select * FROM event.event
             WHERE event_id IN
             (SELECT  A.event_id from event.attendees as A WHERE A.attendee_id='{attendee_id}')"""
        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()

        return result

    @ staticmethod
    def create_event(event_info, loc_info):
        """create row in events.event
            Params: event_info
                    loc_info
            Returns: dict[str:str]
        """
        # Figure out types of the column
        event_schema = NimbusResource._get_table_schema('event')
        # get which columns have values
        valid_columns = [key for key in event_info if event_info[key]]

        sql_event = f"""INSERT INTO event.event ("""
        for col in valid_columns:
            if col == valid_columns[-1]:
                sql_event += f"{col}) "
            else:
                sql_event += f"{col}, "

        sql_event += "VALUES ("
        for col in valid_columns:
            val = event_info[col]
            val_sql = NimbusResource._create_stmt_from_type(
                event_schema[col], val)
            if col == valid_columns[-1]:
                sql_event += val_sql + ')'
            else:
                sql_event += val_sql + ', '

        print('sql of event: ')
        print(sql_event)

        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql_event)
        result_event = cur.fetchone()

        cur.execute("SELECT LAST_INSERT_ID()")
        event_id = cur.fetchone()['LAST_INSERT_ID()']

        # Figure out types of the column
        loc_schema = NimbusResource._get_table_schema('location')
        # get which columns have values
        valid_columns = ['event_id'] + \
            [key for key in loc_info if loc_info[key]]

        sql_loc = f"""INSERT INTO event.location ("""
        for col in valid_columns:
            if col == valid_columns[-1]:
                sql_loc += f"{col}) "
            else:
                sql_loc += f"{col}, "

        sql_loc += "VALUES ("
        for col in valid_columns:
            if col == 'event_id':
                val = f"{event_id}"
            else:
                val = loc_info[col]
            val_sql = NimbusResource._create_stmt_from_type(
                loc_schema[col], val)
            if col == valid_columns[-1]:
                sql_loc += val_sql + ')'
            else:
                sql_loc += val_sql + ', '

        print('loc sql ' + sql_loc)
        cur.execute(sql_loc)
        result_info = cur.fetchone()

        return {'event': result_event, 'location': result_info}

    @ staticmethod
    def update_event(event_id, event_info, loc_info):
        """ Update event in events.event
        """
        # Figure out types of the column
        event_schema = NimbusResource._get_table_schema('event')
        # get which columns have values
        valid_columns = [key for key in event_info if event_info[key]]

        sql_event = f"""UPDATE event.event SET """
        for col in valid_columns:
            val = event_info[col]
            if col == valid_columns[-1]:
                sql_event += f"""{col}={NimbusResource._create_stmt_from_type(
                event_schema[col], val)}"""
            else:
                sql_event += f"""{col}={NimbusResource._create_stmt_from_type(
                event_schema[col], val)}, """

        sql_event += f" WHERE event_id={event_id}"
        print('sql of event: ')
        print(sql_event)

        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql_event)

        # Figure out types of the column
        loc_schema = NimbusResource._get_table_schema('location')
        # get which columns have values
        valid_columns = [key for key in loc_info if loc_info[key]]

        sql_loc = f"""UPDATE event.location SET """
        for col in valid_columns:
            val = loc_info[col]
            if col == valid_columns[-1]:
                sql_loc += f"""{col}={NimbusResource._create_stmt_from_type(
                loc_schema[col], val)}"""
            else:
                sql_loc += f"""{col}={NimbusResource._create_stmt_from_type(
                loc_schema[col], val)}, """

        sql_loc += f" WHERE event_id={event_id}"
        print('sql of loc; ' + sql_loc)
        cur.execute(sql_loc)
        
        msg = json.dumps(event_info)
        msg = publish_message_to_sns(msg)
        return True

    @ staticmethod
    def delete_event(event_id):
        """ Deletes event from event db by event_id
        """
        sql = f"""DELETE FROM event.event WHERE event_id={event_id}"""

        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)

        return res

    @ staticmethod
    def register_for_event(attendee_id, event_id):
        """ Registers an attendee for an event by event_id, attendee_id
        """
        sql = f"""INSERT INTO event.attendees
        VALUES ({event_id}, '{attendee_id}')
        """
        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql)

        return True

    @ staticmethod
    def unregister_for_event(attendee_id, event_id):
        """ Unregisters an attendee for an event by event_id, attendee_id
        """
        sql = f"""DELETE FROM
                event.attendees
                WHERE attendee_id='{attendee_id}' AND event_id={event_id}"""

        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        cur.execute(sql)

        return True
