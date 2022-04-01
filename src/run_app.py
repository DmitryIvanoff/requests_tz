from concurrent.futures import ProcessPoolExecutor

import tornado.ioloop
import tornado.process
from tornado.options import options, parse_command_line

import app.settings
from app.app import main

if __name__ == "__main__":
    parse_command_line()
    if options.local:
        app.settings.DATABASE_URL = app.settings.DATABASE_URL_LOCAL
    loop = tornado.ioloop.IOLoop.current()
    executor = ProcessPoolExecutor()
    loop.set_default_executor(executor)
    try:
        loop.run_sync(main)
    finally:
        executor.shutdown(wait=True)
