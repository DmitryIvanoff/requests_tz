import base64
import logging
from functools import partial
from marshmallow import Schema, fields, post_load, validate
from app.models import Request

import tornado.ioloop

logger = logging.getLogger("app")


class RequestSchema(Schema):
    key = fields.Str(required=True, allow_none=False)
    body = fields.Dict(allow_none=True)
    amount = fields.Int(dump_only=True)

    @staticmethod
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

    @post_load
    def create(self, data, **kwargs):
        return Request(**data)
