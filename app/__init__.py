from flask import Flask
from flask_restful import Api

from app.schema import db, ma
from app.api import BookmarksResource, BookmarkResource, TestResource

import sys

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    """
    if len(sys.argv) > 1:
        s = app.config["SQLALCHEMY_DATABASE_URI"]
        app.config["SQLALCHEMY_DATABASE_URI"] = s.replace(
            s[ s.find('@')+1 : s.find(':', s.find('@')+1) ], 
            sys.argv[1]
        )
    """
    db.init_app(app)
    api = Api(app)
    ma.init_app(app)
    with app.app_context():
        db.create_all()
    api.add_resource(BookmarksResource, '/bookmarks')
    api.add_resource(BookmarkResource, '/bookmarks/<bookmark_id>')
    api.add_resource(TestResource, '/test')
    return app
