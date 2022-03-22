import os
import databases
import tornado.web
import tornado.ioloop
import tornado.locks
import tornado.netutil
import tornado.process
from tornado.options import options
from tornado.web import url
from tornado.routing import HostMatches

from app import settings
from app.handlers import RequestsReadUpdateDeleteHandler, RequestsCreateListHandler


class App(tornado.web.Application):
    def __init__(self, db, *args, **kwargs):
        self.db: databases.Database = db

        handlers = [
            (
                HostMatches(r"(localhost|127\.0\.0\.1)"),
                [
                    (r"/requests/([^/]+)/?", RequestsReadUpdateDeleteHandler),
                    (r"/requests/", RequestsCreateListHandler),
                ],
            )
        ]
        app_settings = dict(
            base_dir=os.path.dirname(__file__),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret=settings.SECRET_KEY,
        )
        super().__init__(handlers, **app_settings, **kwargs)


async def main():
    async with databases.Database(settings.DATABASE_URL) as database:
        app = App(
            database,
            debug=options.debug,
        )
        app.listen(options.port)

        shutdown_event = tornado.locks.Event()

        await shutdown_event.wait()
