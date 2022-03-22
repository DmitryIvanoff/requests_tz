import tornado.ioloop
import tornado.process
from tornado.options import parse_command_line
from concurrent.futures import ProcessPoolExecutor
from app.app import main

if __name__ == "__main__":
    parse_command_line()
    loop = tornado.ioloop.IOLoop.current()
    executor = ProcessPoolExecutor()
    loop.set_default_executor(executor)
    try:
        loop.run_sync(main)
    finally:
        executor.shutdown(wait=True)
