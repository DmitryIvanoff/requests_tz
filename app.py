import tornado.web
import tornado.ioloop
import tornado.locks
import tornado.netutil
import tornado.process
from tornado.options import options
from tornado.web import url

from concurrent.futures import ProcessPoolExecutor

import os
import settings
import databases

from handlers import (RequestsReadUpdateDeleteHandler, RequestsCreateHandler)


class App(tornado.web.Application):
    def __init__(self, db, *args, **kwargs):
        self.db: databases.Database = db

        handlers = [
            url(r"/requests/([^/]+)/?", RequestsReadUpdateDeleteHandler),
            url(r"/requests/", RequestsCreateHandler),
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


if __name__ == "__main__":
    loop = tornado.ioloop.IOLoop.current()
    executor = ProcessPoolExecutor()
    loop.set_default_executor(executor)
    try:
        loop.run_sync(main)
    finally:
        executor.shutdown(wait=True)

