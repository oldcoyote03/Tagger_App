""" Main app module """

import os
import logging
from logging import config as logging_config
from flask import Flask
from app.config import get_config
from app.config.utils import get_logging_config
from app.schema import db, ma
from app.api import register_healthcheck, register_api
from app.services import BookmarksService


def create_app(config_name=None):
    """ Create the app """
    config_obj = get_config(config_name)
    logging_config.dictConfig(get_logging_config(os.environ.get("LOGGING_FILE")))
    log = logging.getLogger("create_app")
    log.info(f"Configuring app as {config_obj.NAME}...")
    app = Flask(__name__)
    app.config.from_object(config_obj)
    db.init_app(app)
    ma.init_app(app)
    register_healthcheck(app)
    register_api(app, BookmarksService)
    return app
