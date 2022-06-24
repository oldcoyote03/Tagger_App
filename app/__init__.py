import os
from flask import Flask
from flask_restful import Api

from app.schema import db, ma
from app.api import BookmarksResource

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    db.init_app(app)
    api = Api(app)
    ma.init_app(app)
    api.add_resource(BookmarksResource, '/bookmarks')
    return app
