from flask import request
from flask_restplus import Resource
from Ressources.swagger_api import api
from API.OpenRequestCache.business import get_open_request_cache
from API.OpenRequestCache.models import open_request_cache_input

ns = api.namespace('open_request_cache', description='Abstract cache for any open request')


@ns.route('/')
class OpenRequestCacheCollection(Resource):
    @ns.response(200, '{product_data}')
    @ns.expect(open_request_cache_input)
    def get(self):
        """
        This route will cache the result of a request and use the cache when there is one regardless of the result of the request.
        """
        return get_open_request_cache(request)
