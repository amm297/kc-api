import os
import pickle

import numpy as np
from flask_restful import Resource, reqparse

from helpers.db_connection import DBConnection
from helpers.gcloud_connection import download_file


class RecommenderRestaurantController(Resource):
    MAX_RESULTS = os.getenv('MAX_RESULTS', 5)
    parser = reqparse.RequestParser()
    parser.add_argument('lat', type=float)
    parser.add_argument('lng', type=float)
    parser.add_argument('review', type=float)
    parser.add_argument('tags', type=list)

    def __init__(self):
        super(RecommenderRestaurantController, self).__init__()
        self.rlf = download_file('models/kmeans_coords.pkl') if os.getenv("LOCAL",
                                                                          False) else 'models/kmeans_coords.pkl'
        self.recommender_location = pickle.load(open(self.rlf, "rb"))
        print('location recommender loaded')

        self.rrf = download_file('models/kmeans_review.pkl') if os.getenv("LOCAL",
                                                                          False) else 'models/kmeans_review.pkl'
        self.recommender_review = pickle.load(open(self.rrf, "rb"))
        print("rate recommender loaded")

        self.rtf = download_file('models/kmeans_tags .pkl') if os.getenv("LOCAL",
                                                                         False) else 'models/kmeans_tags.pkl'
        self.recommender_tags = pickle.load(open(self.rtf, "rb"))
        print("rate recommender loaded")

    def post(self):
        print('--------GENERATE RECOMMENDATION--------')
        args = self.parser.parse_args()
        cluster_location = \
            self.recommender_location.predict(np.array([args.get('lng'), args.get('lat')]).reshape(1, -1))[0]
        cluster_review = self.recommender_review.predict(np.array([args.get('review')]).reshape(1, -1))[0]
        cluster_tags = self.recommender_tags.predict(np.array([args.get('tags')]).reshape(1, -1))[0]
        print(f'clusters obtained')
        return self.__recommend_restaurants(cluster_location, cluster_review, cluster_tags, args.get('lat'),
                                            args.get('lng'))

    def __recommend_restaurants(self, cluster_location, cluster_review, cluster_tags, lat, lng):
        db = DBConnection()
        print('connected')
        results = db.execute_query(
            f'SELECT title, address, type, rating, reviews as review, latitude, longitude, price, description, tags, ( 2 * asin(sqrt(cos(radians({lat})) * cos(radians(r.latitude)) * pow(sin(radians(({lng} - r.longitude) / 2)), 2) + pow(sin(radians(({lat} - r.latitude) / 2)), 2))) *6371) AS distance FROM restaurants r WHERE  cluster_location = \'{cluster_location}\' AND cluster_rate = \'{cluster_review}\' AND cluster_tags = \'{cluster_tags}\' ORDER BY distance ASC LIMIT {self.MAX_RESULTS}')

        return {"restaurants": results} if results else {}
