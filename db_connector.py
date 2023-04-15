import mysql.connector.pooling
import os
from dotenv import load_dotenv

load_dotenv()
class Database:
    def __init__(self, pool_size=5):
        self.config = {
            "host": os.getenv("MYSQL_HOST"),
            "user": os.getenv("MYSQL_USER"),
            "password": os.getenv("MYSQL_PASS"),
            "database": os.getenv("MYSQL_DB"),
            "pool_name": "mypool",
            "pool_size": pool_size,
        }
        self.cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**self.config)

    def execute(self, query, params=None):
        try:
            cnx = self.cnx_pool.get_connection()
            cursor = cnx.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result

    def execute_update(self, query, params=None):
        try:
            cnx = self.cnx_pool.get_connection()
            cursor = cnx.cursor(buffered=True)
            cursor.execute(query, params)
            cnx.commit()
            rowcount = cursor.rowcount
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            rowcount = None
        finally:
            cursor.close()
            cnx.close()
        return rowcount
    def execute_proc(self, query, params=None):
        try:
            cnx = self.cnx_pool.get_connection()
            cursor = cnx.cursor(buffered=True)
            cursor.callproc(query, params)
            for result in cursor.stored_results():
                final_result = result.fetchall()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            result = None
        finally:
            cursor.close()
            cnx.close()
        return final_result

