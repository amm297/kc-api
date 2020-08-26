import json


class Apartment:
    def __init__(self, values):
        self.id = values[0]
        self.url = values[1]
        self.name = values[2]
        self.description = values[3]
        self.house_rules = values[4]
        self.picture_url = values[5]
        self.property_type = values[6]
        self.room_type = values[7]
        self.accommodates = values[8]
        self.bathrooms = values[9]
        self.bedrooms = values[10]
        self.beds = values[11]
        self.bed_type = values[12]
        self.amenities = values[13]
        self.square_feet = values[14]
        self.street = values[15]
        self.neighbourhood = values[16]
        self.zipcode = values[17]
        self.latitude = values[18]
        self.longitude = values[19]
        self.price = values[20]
        self.security_deposit = values[21]
        self.cleaning_fee = values[22]
        self.cancellation_policy = values[23]
        self.number_of_reviews = values[24]
        self.review_scores_rating = values[25]
        self.review_scores_accuracy = values[26]
        self.review_scores_cleanliness = values[27]
        self.review_scores_checkin = values[28]
        self.review_scores_communication = values[29]
        self.review_scores_location = values[30]
        self.review_scores_value = values[31]

    def to_json(self):
        return json.dumps(self.__dict__)
