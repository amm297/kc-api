import os

from flask_restful import Resource


class Hello(Resource):
    def get(self, name):
        aux = os.getenv('TEST')
        MYSQL_HOST = os.getenv('MYSQL_HOST')
        MYSQL_USER = os.getenv('MYSQL_USER')
        MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
        MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
        return {"Hello": f"{name} {aux} {MYSQL_HOST} {MYSQL_USER} {MYSQL_PASSWORD} {MYSQL_DATABASE}"}
