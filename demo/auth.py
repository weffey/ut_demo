import json
from uuid import uuid4

import falcon
from sqlalchemy import text

class RegisterResource(object):
    def on_post(self, req, resp):
        req.session.execute(
            text(
                """
                INSERT INTO users (
                    id,
                    username,
                    password
                )
                VALUES (
                    :id,
                    :username,
                    :password
                );
                """
            ),
            params=dict(
                id=str(uuid4()),
                username=req.context['doc'].get('username'),
                password=req.context['doc'].get('password'),
            ),
        )
        resp.status = falcon.HTTP_201
        resp.context['result'] = {
            "msg": "hello {username}!".format(
                username=req.context['doc'].get('username') or 'unkown'
            ),
        }
        resp.content_type = falcon.MEDIA_JSON
