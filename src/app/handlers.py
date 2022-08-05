import json
import logging
from functools import partial
from typing import Union

import databases
import tornado.ioloop
import tornado.web
from marshmallow.exceptions import ValidationError
from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from app.models import Request
from app.schemas import RequestSchema

logger = logging.getLogger("app")


class BaseHandler(tornado.web.RequestHandler):
    schema = RequestSchema
    model = Request

    def get_schema(self):
        return self.schema

    def get_model(self):
        return self.model

    def prepare(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None

    async def fetch_entity(self, key: str) -> Union[dict, None]:
        db: databases.Database = self.application.db
        model = self.get_model()
        schema = self.get_schema()
        query = select(model).where(model.key == key)
        result = await db.fetch_one(query)
        logger.debug(f"query: {query}\nresult: {result}")
        return schema().dump(result) if result else None


class RequestsReadUpdateDeleteHandler(BaseHandler):
    async def get(self, key: str):
        """
        get Request object
        :param key:
        :return:
        """
        result = await self.fetch_entity(key)
        if result:
            self.write(result)
            self.set_status(200)
        else:
            raise tornado.web.HTTPError(404)

    async def delete(self, key: str):
        """
        delete Request object
        :param key:
        :return:
        """
        db: databases.Database = self.application.db
        model = self.get_model()
        query = delete(model).where(model.key == key)
        result = await db.execute(query)
        logger.debug(f"query: {query}\nresult: {result}")
        self.set_status(204, "No content")


class RequestsCreateListHandler(BaseHandler):
    async def get(self):
        """
        list all Request objs
        :return:
        """
        db: databases.Database = self.application.db
        model = self.get_model()
        schema = self.get_schema()
        query = select(model)
        result = await db.fetch_all(query)
        logger.debug(f"query: {query}\nresult: {result}")
        await self.finish(schema().dumps(result, many=True) if result else None)

    async def post(self):
        """
        create new Request object
        :return:
        """
        db: databases.Database = self.application.db
        schema = self.get_schema()
        model = self.get_model()
        logger.debug(self.request.body)
        body = self.json_args
        if not body:
            self.set_status(200, "Ok")
            await self.finish({})
            return

        # generate key
        ioloop = tornado.ioloop.IOLoop.current()
        key = await ioloop.run_in_executor(None, partial(schema.generate_key, body))
        logger.debug(key)

        # validation
        try:
            validated_data: Request = schema().load({"key": key, "body": body})
        except ValidationError:
            raise tornado.web.HTTPError(400)

        # check that key in db then update if not insert
        query = insert(model).values(
            key=validated_data.key, body=validated_data.body, amount=1
        ).on_conflict_do_update(
            constraint='requests_pk',
            set_=dict(amount=model.amount + 1)
        ).returning('*')
        result = await db.execute(query)
        logger.debug(f"query: {query}\nresult: {result}")
        self.set_status(200, "Ok")
