import pymysql

import os


class NimbusResource:
    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        user = os.environ.get("DBUSER")
        pw = os.environ.get("DBPW")
        host = os.environ.get("DBHOST")

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

    @staticmethod
    def get_events():
        """ Gets all events in event.event
            Returns: all events
        """
        sql = "SELECT * FROM event.event"
        conn = NimbusResource._get_connection()
        cur =  conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchone()

        return result


    @staticmethod
    def get_event_info(id):
        """Returns from event.event join event.attendees
            Params: event_id
            Returns: event information and ticket information
        """
        sql = "SELECT * FROM event.e JOIN event.attendees AS A WHERE E.event_id=%s"
        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, (id))
        result = cur.fetchone()

        return result

    @staticmethod
    def get_event_attendees(id):
        """Gets event information & ticket information
            Params: event_id
            Returns: attendee information
        """
        sql = "SELECT * FROM event.event JOIN event.attendees ON event_id JOIN attendees.info ON attendee_id WHERE event_id =%s"
        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, (id))
        result = cur.fetchone()

        return result

    @staticmethod
    def create_event(event_info, loc_info):
        """create row in events.event 
            Params: event_info
                    loc_info
            Returns: dict[str:str]
        """
        
        sql_event = f"""INSERT INTO event.event ("""
        # get which columns have values
        valid_columns = [key for key in event_info if not event_info[key]]
        for col in valid_columns:
            sql_event += f"col, "
        sql_event += ") VALUES ("
        # column values with info
        for col in valid_columns:
            sql_event += f"{event_info[col], }"
        sql_event += ")"

        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql_event, args=id)
        result_event = cur.fetchone()

        sql_location = f"""INSERT INTO event.location"""
        # get which columns have values
        valid_columns = [key for key in loc_info if not loc_info[key]]
        for col in valid_columns:
            sql_event += f"col, "
        sql_location += ") VALUES ("
        # column values with info
        for col in valid_columns:
            sql_event += f"{loc_info[col], }"
        sql_location += ")"

        res = cur.execute(sql_location, args=id)
        result_event = cur.fetchone()

        return {'event': result_event, 'location': loc_info}

    @staticmethod
    def update_event(info):
        """
        update event in events.event
        """
        sql = f"""UPDATE event.event SET """
        for key in info:
            if info[key] != "":
                sql += f"{key}={info[key]}"
        sql += f"WHERE event_id={info.event_id}"

        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=id)
        result = cur.fetchone()

        return result

    @staticmethod
    def delete_event(event_id):
        """ Deletes event from event db by event_id
        """        
        sql = f"""DELETE FROM event.event WHERE event_id={event_id}"""

        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=id)
        result = cur.fetchone()

        return result

    @staticmethod
    def register_for_event(attendee_id, event_id):
        """ Registers an attendee for an event by event_id, attendee_id
        """
        sql = f"""INSERT INTO event.attendees
        VALUES ({event_id}, {attendee_id})
        """
        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=id)
        result = cur.fetchone()

        return result