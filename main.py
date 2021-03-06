from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from controller.appartment import ApartmentController
from controller.location import LocationController
from controller.recommender import RecommenderController
from controller.tags import TagController
from hello import Hello

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Hello, '/hello/<name>')
api.add_resource(LocationController, '/locations')
api.add_resource(TagController, '/tags')
api.add_resource(ApartmentController, '/apartments/<neighborhood>/<pax>')
api.add_resource(RecommenderController, '/recommender')

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
