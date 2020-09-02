import json


class Restaurant:
    def __init__(self, values):
        self.title = values[0]
        self.address = values[1]
        self.distance = values[2]

    def to_json(self):
        return json.dumps(self.__dict__)
