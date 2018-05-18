import logging
import falcon

from demo.auth import RegisterResource
from demo.config import CONN_STR
from demo.exceptions import ValidationError
from demo.middleware import (
    JSONTranslator,
    RequireJSON,
    SqlLiteConnection,
)


def internal_error_handler(e, req, resp, params):
    # Why is this logging a bad idea?

    if hasattr(req, 'context'):
        logging.debug('internal_error_handler: %s --> %s', e, req.context)
    if hasattr(req, 'params'):
        logging.debug('internal_error_handler: %s --> %s', e, req.params)
    if isinstance(e, ValidationError):
        resp.status = falcon.HTTP_400
        resp.context['result'] = {
            "errors": e.errors,
        }
        resp.content_type = falcon.MEDIA_JSON
        logging.info('validation failed: %s --> %s', req.url, e.errors)
        return
    logging.exception(e)
    raise e


api = application = falcon.API(
    middleware=[
        RequireJSON(),
        JSONTranslator(),
        SqlLiteConnection(conn_str=CONN_STR),
    ],
)
api.add_error_handler(Exception, internal_error_handler)


class RootResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.context['result'] = {
            "msg": "hello world!",
        }
        resp.content_type = falcon.MEDIA_JSON

api.add_route('/', RootResource())
api.add_route('/register', RegisterResource())
