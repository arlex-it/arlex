from Ressources.swagger_api import api
from flask_restplus import fields

open_request_cache_input = api.parser()
open_request_cache_input.add_argument('url', location='path')
