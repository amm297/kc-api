from flask_restful import Resource

from domain.apartment import Apartment
from helpers.db_connection import DBConnection


class ApartmentController(Resource):
    def get(self, neighborhood, pax):
        print(pax)
        db = DBConnection()
        results = db.execute_query(
            f'SELECT id, listing_url, name, description, house_rules, picture_url, property_type, room_type, accommodates, bathrooms, bedrooms, beds, bed_type, amenities, square_feet, street, neighbourhood, zipcode, latitude, longitude, price, security_deposit, cleaning_fee, cancellation_policy, number_of_reviews, review_scores_rating, review_scores_accuracy, review_scores_cleanliness, review_scores_checkin, review_scores_communication, review_scores_location, review_scores_value FROM airbnb WHERE neighbourhood = \'{neighborhood}\'')
        if results:
            apartments = [Apartment(apartment).to_json() for apartment in results]
            return {"apartments": apartments}
        return {}
