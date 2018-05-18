import json

import falcon

from auth import RegisterResource
from middleware import (
    JSONTranslator,
    RequireJSON,
    SqlLiteConnection,
)

api = application = falcon.API(middleware=[
    RequireJSON(),
    JSONTranslator(),
    SqlLiteConnection(),
])


class RootResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.context['result'] = {
            "msg": "hello world!",
        }
        resp.content_type = falcon.MEDIA_JSON

api.add_route('/', RootResource())
api.add_route('/register', RegisterResource())
