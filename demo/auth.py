from uuid import uuid4

import falcon
from sqlalchemy import text

from demo.exceptions import ValidationError

class LoginResource(object):
    def on_post(self, req, resp):
        errors = []

        if not (req.context['doc'].get('username') or '').strip():
            errors.append({
                "field": "username",
                "msg": "Username is required",
            })

        if not (req.context['doc'].get('password') or '').strip():
            errors.append({
                "field": "password",
                "msg": "Password is required",
            })

        if errors:
            raise ValidationError(errors=errors)

        results = req.session.execute(
            text(
                """
                SELECT *
                FROM users
                WHERE
                    username = :username
                    AND password = :password
                ;
                """
            ),
            params=dict(
                username=req.context['doc'].get('username'),
                password=req.context['doc'].get('password'),
            ),
        ).fetchone()

        if not results:
            raise ValidationError(errors=[{
                "field": "username",
                "msg": "Account not found",
            }])

        resp.status = falcon.HTTP_200
        resp.context['result'] = {
            "msg": "hello {username}!".format(
                username=req.context['doc'].get('username') or 'unkown'
            ),
            "id": results[0]
        }
        resp.content_type = falcon.MEDIA_JSON


class RegisterResource(object):
    def on_post(self, req, resp):
        errors = []

        if not (req.context['doc'].get('username') or '').strip():
            errors.append({
                "field": "username",
                "msg": "Username is required",
            })
        else:
            if len(req.context['doc']['username']) < 3:
                errors.append({
                    "field": "username",
                    "msg": "Username must be more than 3 characters",
                })
            elif len(req.context['doc']['username']) > 50:
                errors.append({
                    "field": "username",
                    "msg": "Username must be less than 50 characters",
                })

        if not (req.context['doc'].get('password') or '').strip():
            errors.append({
                "field": "password",
                "msg": "Password is required",
            })
        else:
            if len(req.context['doc']['password']) < 10:
                errors.append({
                    "field": "password",
                    "msg": "Password must be more than 10 characters",
                })
            elif len(req.context['doc']['password']) > 20:
                errors.append({
                    "field": "password",
                    "msg": "Password must be less than 20 characters",
                })

        if errors:
            raise ValidationError(errors=errors)

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
