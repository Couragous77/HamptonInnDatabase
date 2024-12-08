import mysql.connector

class DatabaseManager:
    def __init__(self, db_config):
        self.db_config = db_config

    def connect(self):
        return mysql.connector.connect(**self.db_config)

    def execute_query(self, query, params=None, fetch=False):
        try:
            conn = self.connect()
            cursor = conn.cursor(dictionary=True if fetch else False)
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            conn.commit()
        except mysql.connector.Error as err:
            raise Exception(f"Database Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
