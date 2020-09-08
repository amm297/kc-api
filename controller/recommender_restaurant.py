import os
import pickle

import numpy as np

from helpers.db_connection import DBConnection
from helpers.gcloud_connection import download_file


class RecommenderRestaurant():

    def __init__(self, max_results):
        self.MAX_RESULTS = max_results
        self.rlf = download_file('models/kmeans_coords.pkl') if os.getenv("LOCAL",
                                                                          False) else 'models/kmeans_coords.pkl'
        self.recommender_location = pickle.load(open(self.rlf, "rb"))
        print('location recommender loaded')

        self.rrf = download_file('models/kmeans_review.pkl') if os.getenv("LOCAL",
                                                                          False) else 'models/kmeans_review.pkl'
        self.recommender_review = pickle.load(open(self.rrf, "rb"))
        print("rate recommender loaded")

        self.rtf = download_file('models/kmeans_tags.pkl') if os.getenv("LOCAL",
                                                                        False) else 'models/kmeans_tags.pkl'
        self.recommender_tags = pickle.load(open(self.rtf, "rb"))

        self.rtvf = download_file('models/kmeans_tags_vectorizer.pkl') if os.getenv("LOCAL",
                                                                                    False) else 'models/kmeans_tags_vectorizer.pkl'
        self.recommender_tags_vectorizer = pickle.load(open(self.rtvf, "rb"))
        print("rate recommender loaded")

    def recommend(self, lat, lng, review, tags):
        print('--------GENERATE RESTAURANT RECOMMENDATION--------')

        cluster_location = self.recommender_location.predict(np.array([lng, lat]).reshape(1, -1))[0]
        cluster_review = self.recommender_review.predict(np.array([review]).reshape(1, -1))[0]
        cluster_tags = None
        if tags:
            tags_vectorized = self.recommender_tags_vectorizer.transform([tags])
            cluster_tags = self.recommender_tags.predict(tags_vectorized)[0]

        print('--------GENERATED RESTAURANT RECOMMENDATION--------')
        return self.__recommend_restaurants(cluster_location, cluster_review, cluster_tags, lat, lng)

    def __recommend_restaurants(self, cluster_location, cluster_review, cluster_tags, lat, lng):
        db = DBConnection()
        print('connected')
        results = db.execute_query(
            f'SELECT title, address, type, rating, reviews as review, latitude, longitude, price, description, tags, ( 2 * asin(sqrt(cos(radians({lat})) * cos(radians(r.latitude)) * pow(sin(radians(({lng} - r.longitude) / 2)), 2) + pow(sin(radians(({lat} - r.latitude) / 2)), 2))) *6371) AS distance FROM restaurants r WHERE  cluster_location = \'{cluster_location}\' AND cluster_rate = \'{cluster_review}\' {self.__has_cluster_tag(cluster_tags)} ORDER BY distance DESC LIMIT {self.MAX_RESULTS}')

        return {"restaurants": results} if results else {}

    def __has_cluster_tag(self, cluster_tags):
        if cluster_tags:
            " AND cluster_tags= \'" + cluster_tags + "\' "
        else:
            return ''
