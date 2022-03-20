import os
import logging.config
from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=bool(os.environ.get('DEBUG', True)), help="run in debug mode", type=bool)
define("db_host", default=os.environ.get('DB_HOST', '127.0.0.1'), help="db host")
define("db_port", default=os.environ.get('DB_PORT', '5432'), help="db port")
define("db_database", default=os.environ.get('DB_NAME', "requests"), help="db name")
define("db_user", default=os.environ.get('DB_USER', 'requests'), help="db user")
define("db_password", default=os.environ.get('DB_PASSWORD', 'requests'), help="db password")
define("loglevel", default="INFO", help="logging level")
define("local", default=bool(os.environ.get('LOCAL', False)), help="local deploy")

parse_command_line()

# ------ SETTINGS ------
# todo: refactor settings
SECRET_KEY = os.environ.get("SECRET_KEY", "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__")

DATABASE_URL_LOCAL = "sqlite:///./test.db"

DATABASE_URL = f"postgresql://{options.db_user}:{options.db_password}" \
                   f"@{options.db_host}:{options.db_port}/{options.db_database}?min_size=5"

if options.local:
    DATABASE_URL = DATABASE_URL_LOCAL

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'app': {
            'handlers': ['console'],
            'level': options.loglevel,
        },
    },
}

logging.config.dictConfig(LOGGING)
