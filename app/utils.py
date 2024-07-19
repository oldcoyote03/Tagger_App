""" App Utilities """

import logging
from logging import config as logging_config

from flask import Flask
from flask_restful import Api

from app.schema import db, ma
from app.api import BookmarksResource, BookmarkResource, TestResource
from app.config import get_logging_config

def create_app():
    """ Create the app """
    app = Flask(__name__)
    app.config.from_object("settings")
    logging_config.dictConfig(get_logging_config(app.config.get("LOG_FILE")))
    logger = logging.getLogger("create_app")
    logger.info("Configuring app...")
    db.init_app(app)
    flask_api = Api(app)
    ma.init_app(app)
    flask_api.add_resource(BookmarksResource, '/bookmarks')
    flask_api.add_resource(BookmarkResource, '/bookmarks/<bookmark_id>')
    flask_api.add_resource(TestResource, '/test')
    return app
