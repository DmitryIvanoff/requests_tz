import tornado.web
import tornado.ioloop
import databases
import json
import base64
import logging
from functools import partial
from sqlalchemy import insert, select, update, delete

from app.models import Request

logger = logging.getLogger('app')


def generate_key(body: dict) -> str:
    stack = [body]
    keys_stack = []
    while stack:
        element = stack.pop()
        if isinstance(element, list):
            stack.extend(element)
        elif isinstance(element, dict):
            for kv in element.items():
                stack.extend(kv)
        else:
            keys_stack.append(str(element))
    return base64.b64encode("".join(reversed(keys_stack)).encode()).decode()


class BaseHandler(tornado.web.RequestHandler):
    async def fetch_entity(self, key: str) -> dict:
        db: databases.Database = self.application.db
        query = select(Request).where(Request.key == key)
        result = await db.fetch_one(query)
        logger.debug(f'query: {query}\nresult: {result}')
        return dict(result) if result else None


class RequestsReadUpdateDeleteHandler(BaseHandler):
    def prepare(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None
        self.set_header('Content-Type', 'application/json')

    async def get(self, key):
        result = await self.fetch_entity(key)
        if result:
            self.write(json.dumps(result))
            self.set_status(200)
        else:
            raise tornado.web.HTTPError(404)

    async def delete(self, entity):
        db: databases.Database = self.application.db
        query = delete(Request).where(Request.key == entity)
        result = await db.execute(query)
        logger.info(f'query: {query}\nresult: {result}')
        self.set_status(204, "No content")



class RequestsCreateHandler(BaseHandler):
    def prepare(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None
        self.set_header('Content-Type', 'application/json')

    async def post(self):
        db: databases.Database = self.application.db
        logger.debug(self.request.body)
        body = self.json_args
        if not body:
            self.set_status(200, 'Ok')
            self.write({})
            return

        ioloop = tornado.ioloop.IOLoop.current()
        key = await ioloop.run_in_executor(None, partial(generate_key, body))
        logger.debug(key)

        # check that key in db then update if not insert
        async with db.transaction(isolation="read_committed"):
            entity = await self.fetch_entity(key)
            if not entity:
                query = insert(Request).values(key=key, body=body, amount=1)
                result = await db.execute(query)
                logger.debug(f'query: {query}\nresult: {result}')
                self.set_status(201, 'Created')
            else:
                query = update(Request).where(Request.key == key).values(amount=Request.amount + 1)
                result = await db.execute(query)
                logger.debug(f'query: {query}\nresult: {result}')
                self.set_status(200, 'Ok')

        entity = await self.fetch_entity(key)
        self.write(json.dumps(entity))

