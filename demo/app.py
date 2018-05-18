import falcon

from demo.auth import RegisterResource
from demo.config import CONN_STR
from demo.middleware import (
    JSONTranslator,
    RequireJSON,
    SqlLiteConnection,
)

api = application = falcon.API(
    middleware=[
        RequireJSON(),
        JSONTranslator(),
        SqlLiteConnection(conn_str=CONN_STR),
    ],
)

class RootResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.context['result'] = {
            "msg": "hello world!",
        }
        resp.content_type = falcon.MEDIA_JSON

api.add_route('/', RootResource())
api.add_route('/register', RegisterResource())
