import os

import pymysql


class DBConnection():
    def __init__(self):
        if os.getenv("LOCAL", False):
            try:
                self.conn = pymysql.connect(
                    host=os.getenv('MYSQL_HOST'),
                    user=os.getenv('MYSQL_USER'),
                    passwd=os.getenv('MYSQL_PASSWORD'),
                    database=os.getenv('MYSQL_DATABASE')
                )
                self.cursor = self.conn.cursor()
            except Exception as e:
                print(f'Cannot connect to database due to {e}')
        else:
            self.open_connection()

    def open_connection(self):
        unix_socket = '/cloudsql/{}'.format(os.getenv('MYSQL_HOST'))
        try:
            self.conn = pymysql.connect(user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PASSWORD'),
                                        unix_socket=unix_socket, db=os.getenv('MYSQL_DATABASE'),
                                        cursorclass=pymysql.cursors.DictCursor
                                        )
            self.cursor = self.conn.cursor()
        except pymysql.MySQLError as e:
            print(e)

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
