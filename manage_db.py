""" Manage Database """

import os
from logging import config
from app import create_app
from app.schema import manage_db
from app.utils import parse_args
from app.config.utils import get_logging_config

config.dictConfig(get_logging_config(os.environ.get("LOG_FILE")))

if __name__ == '__main__':
    args = parse_args()
    app = create_app(args.env)
    manage_db(app, args)
