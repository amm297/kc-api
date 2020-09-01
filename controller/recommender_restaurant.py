import pickle

import numpy as np
from flask_restful import Resource, reqparse

from helpers.gcloud_connection import gcloud_connection


class RecommenderRestaurantController(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('lat', type=float)
    parser.add_argument('lng', type=float)

    def __init__(self):
        super(RecommenderRestaurantController, self).__init__()
        self.recommender_file = gcloud_connection().download_file('models/kmeans_coords.pkl')
        self.recommender = pickle.load(open(self.recommender_file, "rb"))

    def post(self):
        args = self.parser.parse_args()
        cluster = self.recommender.predict(np.array([args.get('lng'), args.get('lat')]).reshape(1, -1))[0]
        return {}
