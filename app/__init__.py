""" Main app module """

import os
import logging
from logging import config as logging_config

from flask import Flask
from flask_restful import Api

from app.config import get_config
from app.schema import db, ma
from app.api import BookmarksResource, BookmarkResource, HealthcheckResource


logger = logging.getLogger("create_app")

def create_app(config_name=None):
    """ Create the app """
    config_obj = get_config(config_name)
    logger.info(f"Configuring app as {config_obj.NAME}...")
    app = Flask(__name__)
    app.config.from_object(config_obj)
    db.init_app(app)
    flask_api = Api(app)
    ma.init_app(app)
    flask_api.add_resource(BookmarksResource, '/bookmarks')
    flask_api.add_resource(BookmarkResource, '/bookmarks/<bookmark_id>')
    flask_api.add_resource(HealthcheckResource, '/healthcheck')
    return app
