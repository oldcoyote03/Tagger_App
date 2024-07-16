""" App Utilities """

from flask import Flask
from flask_restful import Api

from app.schema import db, ma
from app.api import BookmarksResource, BookmarkResource, TestResource

def create_app():
    """ Create the app """
    app = Flask(__name__)
    app.config.from_object("settings")
    db.init_app(app)
    flask_api = Api(app)
    ma.init_app(app)
    flask_api.add_resource(BookmarksResource, '/bookmarks')
    flask_api.add_resource(BookmarkResource, '/bookmarks/<bookmark_id>')
    flask_api.add_resource(TestResource, '/test')
    print(f"flask app created: {app}\n")
    return app
