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

    # @staticmethod
    # def get_by_key(key):
    #     sql = "SELECT * FROM f22_databases.columbia_student where uni=%s";
    #     conn = ColumbiaStudentResource._get_connection()
    #     cur = conn.cursor()
    #     res = cur.execute(sql, args=key)
    #     result = cur.fetchone()
    #
    #     return result

    @staticmethod
    def get_events():
        sql = "SELECT * FROM event.event where event_id=%s"
        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=id)
        result = cur.fetchone()

        return result

    @staticmethod
    def get_event_info(id):
        # TODO: yamini write a join between event.event and event.tickets
        sql = "SELECT * FROM event.event where event_id=%s"
        conn = NimbusResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=id)
        result = cur.fetchone()

        return result
