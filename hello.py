from flask_restful import Resource


class Hello(Resource):
    def get(self, name):
        return {"Hello": name}
