import tornado.ioloop
import tornado.process
from concurrent.futures import ProcessPoolExecutor
from app.app import main

if __name__ == "__main__":
    loop = tornado.ioloop.IOLoop.current()
    executor = ProcessPoolExecutor()
    loop.set_default_executor(executor)
    try:
        loop.run_sync(main)
    finally:
        executor.shutdown(wait=True)
