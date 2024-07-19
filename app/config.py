""" Configurations """

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