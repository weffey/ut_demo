from uuid import uuid4

import falcon
from sqlalchemy import text

# from demo.exceptions import ValidationError

class RegisterResource(object):
    def on_post(self, req, resp):
        # errors = []

        # if not (req.context['doc'].get('username') or '').strip():
        #     errors.append({
        #         "field": "username",
        #         "msg": "Username is required",
        #     })

        # if not (req.context['doc'].get('password') or '').strip():
        #     errors.append({
        #         "field": "password",
        #         "msg": "Password is required",
        #     })

        # if errors:
        #     raise ValidationError(errors=errors)

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
