import os
import pickle

import numpy as np

from helpers.db_connection import DBConnection
from helpers.gcloud_connection import download_file


class RecommenderPointOfInterest():

    def __init__(self, max_results):
        self.MAX_RESULTS = max_results
        self.rlf = download_file('models/kmeans_poi_coords.pkl') if os.getenv("LOCAL",
                                                                              False) else 'models/kmeans_poi_coords.pkl'
        self.recommender_location = pickle.load(open(self.rlf, "rb"))
        print('location recommender loaded')

    def recommend(self, lat, lng):
        print('--------GENERATE POINT OF INTEREST RECOMMENDATION--------')

        cluster_location = self.recommender_location.predict(np.array([lng, lat]).reshape(1, -1))[0]

        print('--------GENERATED POINT OF INTEREST RECOMMENDATION--------')
        return self.__recommend_restaurants(cluster_location, lat, lng)

    def __recommend_restaurants(self, cluster_location, lat, lng):
        db = DBConnection()
        print('connected')
        results = db.execute_query(
            f'SELECT name, description, schedule, latitude, longitude, ( 2 * asin(sqrt(cos(radians({lat})) * cos(radians(pot.latitude)) * pow(sin(radians(({lng} - pot.longitude) / 2)), 2) + pow(sin(radians(({lat} - pot.latitude) / 2)), 2))) *6371) AS distance FROM point_of_interest pot WHERE  cluster_location = \'{cluster_location}\' ORDER BY distance ASC LIMIT {self.MAX_RESULTS}')

        return {"point_of_interest": results} if results else {}
