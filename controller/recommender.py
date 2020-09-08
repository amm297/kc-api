import os

from flask_restful import Resource, reqparse
from jsonmerge import merge

from controller.recommender_activities import RecommenderActivities
from controller.recommender_poi import RecommenderPointOfInterest
from controller.recommender_restaurant import RecommenderRestaurant


class RecommenderController(Resource):
    MAX_RESULTS = os.getenv('MAX_RESULTS', 5)
    parser = reqparse.RequestParser()
    parser.add_argument('lat', type=float)
    parser.add_argument('lng', type=float)
    parser.add_argument('review', type=float)
    parser.add_argument('tags', type=str)

    def __init__(self):
        super(RecommenderController, self).__init__()
        self.recommender_restaurant = RecommenderRestaurant(self.MAX_RESULTS)
        self.recommender_activities = RecommenderActivities(self.MAX_RESULTS)
        self.recommender_pois = RecommenderPointOfInterest(self.MAX_RESULTS)

    def post(self):
        print('--------GENERATE RECOMMENDATION--------')
        args = self.parser.parse_args()
        restaurants = self.recommender_restaurant.recommend(args.get('lng'), args.get('lat'), args.get('review'),
                                                            args.get('tags'))
        actvities = self.recommender_activities.recommend(args.get('lng'), args.get('lat'), args.get('review'))
        pois = self.recommender_pois.recommend(args.get('lng'), args.get('lat'))

        return merge(merge(restaurants, actvities), pois)
