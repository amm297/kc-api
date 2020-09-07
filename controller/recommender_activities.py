import os
import pickle

import numpy as np

from helpers.db_connection import DBConnection
from helpers.gcloud_connection import download_file


class RecommenderActivities():

    def __init__(self, max_results):
        self.MAX_RESULTS = max_results

        self.rlf = download_file('models/kmeans_act_coords.pkl') if os.getenv("LOCAL",
                                                                              False) else 'models/kmeans_act_coords.pkl'
        self.recommender_location = pickle.load(open(self.rlf, "rb"))
        print('location recommender loaded')

        self.rrf = download_file('models/kmeans_act_review.pkl') if os.getenv("LOCAL",
                                                                              False) else 'models/kmeans_act_review.pkl'
        self.recommender_review = pickle.load(open(self.rrf, "rb"))

    def recommend(self, lat, lng, review):
        print('--------GENERATE ACTIVITIES RECOMMENDATION--------')

        cluster_location = self.recommender_location.predict(np.array([lng, lat]).reshape(1, -1))[0]
        cluster_review = self.recommender_review.predict(np.array([review]).reshape(1, -1))[0]

        print('--------GENERATED ACTIVITIES RECOMMENDATION--------')
        return self.__recommend_restaurants(cluster_location, cluster_review, lat, lng)

    def __recommend_restaurants(self, cluster_location, cluster_review, lat, lng):
        db = DBConnection()
        print('connected')
        results = db.execute_query(
            f'SELECT title, meeting_point, latitude, longitude, rate, review, description, time, language, cancellation, price, ( 2 * asin(sqrt(cos(radians({lat})) * cos(radians(a.latitude)) * pow(sin(radians(({lng} - a.longitude) / 2)), 2) + pow(sin(radians(({lat} - a.latitude) / 2)), 2))) *6371) AS distance FROM activities a WHERE  cluster_location = \'{cluster_location}\' AND cluster_rate = \'{cluster_review}\' ORDER BY distance ASC LIMIT {self.MAX_RESULTS}')

        return {"activities": results} if results else {}
