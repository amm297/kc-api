import json


class Restaurant:
    def __init__(self, values):
        self.title = values[0]
        self.address = values[1]
        self.type = values[2]
        self.rating = values[3]
        self.review = values[4]
        self.latitude = values[5]
        self.longitude = values[6]
        self.price = values[7]
        self.description = values[8]
        self.tags = values[9]
        self.distance = values[10]

    def to_json(self):
        return json.dumps(self.__dict__)
