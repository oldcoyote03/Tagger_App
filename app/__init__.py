import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
from src.api import BookmarksResource

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    db.init_app(app)
    api = Api(app)
    ma.init_app(app)
    api.add_resource(BookmarksResource, '/bookmarks')
    return app
