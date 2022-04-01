import os

from tornado.options import define, options

define("db_host", default=os.environ.get("DB_HOST", "127.0.0.1"), help="db host")
define("db_port", default=os.environ.get("DB_PORT", "5432"), help="db port")
define("db_database", default=os.environ.get("DB_NAME", "requests"), help="db name")
define("db_user", default=os.environ.get("DB_USER", "requests"), help="db user")
define(
    "db_password", default=os.environ.get("DB_PASSWORD", "requests"), help="db password"
)

DATABASE_URL = (
    f"postgresql://{options.db_user}:{options.db_password}"
    f"@{options.db_host}:{options.db_port}/{options.db_database}?min_size=5"
)

DATABASE_URL_LOCAL = "sqlite:///./test.db"
