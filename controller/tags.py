from flask_restful import Resource

from helpers.db_connection import DBConnection


class TagController(Resource):
    def get(self):
        db = DBConnection()
        results = db.execute_query('SELECT tag FROM tags;')
        if results:
            tags = [tag.get('tag') for tag in results]
            return {"tags": tags}
        return {}
