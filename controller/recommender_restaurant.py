import os
import pickle

import numpy as np
from flask_restful import Resource, reqparse

from domain.restaurant import Restaurant
from helpers.db_connection import DBConnection
from helpers.gcloud_connection import gcloud_connection


class RecommenderRestaurantController(Resource):
    MAX_RESULTS = os.getenv('MAX_RESULTS', 5)
    parser = reqparse.RequestParser()
    parser.add_argument('lat', type=float)
    parser.add_argument('lng', type=float)
    parser.add_argument('review', type=float)

    def __init__(self):
        super(RecommenderRestaurantController, self).__init__()
        self.recommender_location_file = gcloud_connection().download_file('models/kmeans_coords.pkl')
        self.recommender_location = pickle.load(open(self.recommender_location_file, "rb"))
        self.recommender_review_file = gcloud_connection().download_file('models/kmeans_review.pkl')
        self.recommender_review = pickle.load(open(self.recommender_review_file, "rb"))

    def post(self):
        args = self.parser.parse_args()
        cluster_location = \
            self.recommender_location.predict(np.array([args.get('lng'), args.get('lat')]).reshape(1, -1))[0]
        cluster_review = self.recommender_review.predict(np.array([args.get('review')]).reshape(1, -1))[0]

        return self.__recommend_restaurants(cluster_location, cluster_review, args.get('lat'), args.get('lng'))

    def __recommend_restaurants(self, cluster_location, cluster_review, lat, lng):
        db = DBConnection()
        results = db.execute_query(
            f'SELECT title, address, ( 2 * asin(sqrt(cos(radians({lat})) * cos(radians(r.latitude)) * pow(sin(radians(({lng} - r.longitude) / 2)), 2) + pow(sin(radians(({lat} - r.latitude) / 2)), 2))) *6371) AS distance FROM restaurants r WHERE  clusterLocation = \'{cluster_location}\' AND clusterRate = \'{cluster_review}\' ORDER BY distance ASC LIMIT {self.MAX_RESULTS}')

        if results:
            restaurants = [Restaurant(restaurant).to_json() for restaurant in results]
            return {"restaurants": restaurants}

        return {}
