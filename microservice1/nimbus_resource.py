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

        conn = pymysql.connect(
            user=user,
            password=pw,
            host=host,
            port=3306,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_event_info(id):
        """Gets event information & ticket information
            Params: event_id
            Returns: event information and ticket information
        """
        sql = "SELECT * FROM event.event JOIN event.attendees WHERE event_id =%s"
        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=id)
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
        res = cur.execute(sql, args=id)
        result = cur.fetchone()

        return result