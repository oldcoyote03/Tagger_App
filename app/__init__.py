""" Main app module """

import logging
from flask import Flask
from app.config import get_config
from app.schema import db, ma
from app.api import register_healthcheck, register_api
from app.services import BookmarksService


logger = logging.getLogger("create_app")

def create_app(config_name=None):
    """ Create the app """
    config_obj = get_config(config_name)
    logger.info(f"Configuring app as {config_obj.NAME}...")
    app = Flask(__name__)
    app.config.from_object(config_obj)
    db.init_app(app)
    ma.init_app(app)
    register_healthcheck(app)
    register_api(app, BookmarksService)
    return app
