import pymysql
import os


class Nimbus_Users:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():

        usr = os.environ.get("DBUSER")
        pw = os.environ.get("DBPW")
        h = os.environ.get("DBHOST")

        conn = pymysql.connect(
            user=usr,
            password=pw,
            host=h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_user_by_uid(uid):
        sql = "SELECT * FROM f22_databases.columbia_students where guid=%s"
        conn = Nimbus_Users._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=uid)
        result = cur.fetchone()
        return result

    @staticmethod
    def get_user_address_by_uid(uid):
        sql = "SELECT * FROM f22_databases.columbia_students where guid=%s"
        conn = Nimbus_Users._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=uid)
        result = cur.fetchone()
        return result
