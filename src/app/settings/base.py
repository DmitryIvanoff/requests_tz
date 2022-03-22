import os
from tornado.options import define, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
define(
    "debug",
    default=bool(os.environ.get("DEBUG", True)),
    help="run in debug mode",
    type=bool,
)

define("local", default=bool(os.environ.get("LOCAL", False)), help="local deploy")


SECRET_KEY = os.environ.get(
    "SECRET_KEY", "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"
)
