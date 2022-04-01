import logging.config

from tornado.options import define, options

define("loglevel", default="INFO", help="logging level")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "app": {
            "handlers": ["console"],
            "level": options.loglevel,
        },
    },
}

logging.config.dictConfig(LOGGING)
