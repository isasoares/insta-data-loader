from flask import Flask
from flask_restful import Api

from .api_resources import LoadProfileData, ProfilePost, ProfileData


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(LoadProfileData, '/<string:username>/upload')
    api.add_resource(ProfilePost, '/<string:username>/<int:post>')
    api.add_resource(ProfileData, '/<string:username>')

    return app
