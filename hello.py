import os

from flask_restful import Resource


class Hello(Resource):
    def get(self, name):
        aux = os.getenv('TEST')
        return {"Hello": name + aux}
