from flask_restful import Resource

from helpers.db_connection import DBConnection


class LocationController(Resource):
    def get(self):
        db = DBConnection()
        results = db.execute_query('SELECT name FROM locations;')
        if results:
            locations = [location.get('name') for location in results]
            return {"locations": locations}
        return {}
