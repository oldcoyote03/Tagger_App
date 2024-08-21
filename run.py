""" Run the app """

import os
import logging
from logging import config
from app import create_app
from app.config.utils import get_logging_config


config.dictConfig(get_logging_config(os.environ.get("LOG_FILE")))
log = logging.getLogger(__name__)

if __name__ == '__main__':
    app = create_app()
    log.info("Starting app...")
    app.run(debug=True, host='0.0.0.0')
