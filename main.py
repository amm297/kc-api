import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from controller.appartment import ApartmentController
from controller.location import LocationController
from controller.recommender_restaurant import RecommenderRestaurantController
from hello import Hello

app = Flask(__name__)
CORS(app)
api = Api(app)

db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASS')
db_name = os.environ.get('DB_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

@app.route('/')

def main():
    # When deployed to App Engine, the `GAE_ENV` environment variable will be
    # set to `standard`
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)

    with cnx.cursor() as cursor:
        cursor.execute('SELECT * FROM airbnb')
        result = cursor.fetchall()
        current_msg = result[0][0]
    cnx.close()

    return str(current_msg)
   
api.add_resource(Hello, '/hello/Holi')
api.add_resource(LocationController, '/locations')
api.add_resource(ApartmentController, '/apartments/<neighborhood>/<pax>')
api.add_resource(RecommenderRestaurantController, '/recommender/restaurant')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]