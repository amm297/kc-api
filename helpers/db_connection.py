import os

import mysql.connector as mysql


class DBConnection():
    def __init__(self):
        try:
            self.conn = mysql.connect(
                host=os.getenv('MYSQL_HOST'),
                user=os.getenv('MYSQL_USER'),
                passwd=os.getenv('MYSQL_PASSWORD'),
                database=os.getenv('MYSQL_DATABASE')
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f'Cannot connect to database due to {e}')

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            self.cursor.close()
            self.conn.close()
            return results
        except Exception as e:
            print(f'Fail to execute query `{query}`')
            return None
