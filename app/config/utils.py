""" 
Configurations for the application 
Target Configurations:
    - Development (default, no persistant storage)
    - Local (persistant storage on local filesystem)
    - Testing (persistant storage on cloud, test database)
    - Production
"""

import os
import logging
from dynaconf import Dynaconf
from app.utils import strtobool, flatten_dict


log = logging.getLogger(__name__)

class Config:
    """ Base Configurations """
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    @staticmethod
    def init_app(app):
        """ Initialize the app """

class DevelopmentConfig(Config):
    """ Development Environment Configurations """
    NAME = "development"

class LocalConfig(Config):
    """ Local Environment Configurations """
    NAME = "local"

class DockerConfig(Config):
    """ Docker Compose Environment Configurations """
    NAME = "docker"

config = {
    "development": DevelopmentConfig,
    "local": LocalConfig,
    "docker": DockerConfig,
    "default": DevelopmentConfig
}

def load_configs(env):
    """ Load the config to OS environment variables """
    settings = Dynaconf(
        environments=False,
        root_path=os.path.join(os.path.dirname(__file__), "env"),
        settings_files=["base.json", f"{env}.json"]
    )
    flattened_settings = Dynaconf(environments=False, **flatten_dict(settings.as_dict()))
    for key, value in flattened_settings.as_dict().items():
        if not os.environ.get(key):
            os.environ[key] = str(value)  # OS environment variables override env json

def get_config(config_name=None):
    """ 
    Config Class Precedence:
        1. Method input
        2. Environment variable
        3. Default --> DevelopmentConfig
    """
    if config_name is not None:
        config_class = config.get(config_name)
    else:
        config_class = config.get(os.environ.get("APP_ENV", "default"))
    env = config_class.NAME
    load_configs(env)
    kwargs = {
        "SQLALCHEMY_DATABASE_URI": os.environ.get("DATABASE_URL"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": strtobool(
            os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", "FALSE")
        ),
    }
    return config_class(**kwargs)

def set_file_handler(handlers, loggers, log_file):
    """ Set logging file handler """
    handlers.update({
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": log_file,
            "maxBytes": 2024 * 2024 * 10,
            "backupCount": 5,
        }
    })
    loggers["default"]["handlers"].append("file")
    loggers["root"]["handlers"].append("file")

def get_logging_config(log_file=None):
    """ Get logging config dictionary """
    log_config = {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {
            "default": {"level": "DEBUG", "handlers": ["console"]},
            "root": {"level": "DEBUG", "handlers": ["console"]}
        },
        "disable_existing_loggers": False,
    }
    if log_file:
        set_file_handler(log_config.get("handlers"), log_config.get("loggers"), log_file)
    return log_config
