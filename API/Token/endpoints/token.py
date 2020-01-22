from flask import request
from flask_restplus import Resource

from API.Utilities.auth import require_authentication
from Ressources.swagger_api import api
from API.Token.business import PostToken
from API.Token.models import token_input, token_param

ns = api.namespace('token', description='mange token')


@ns.route('/')
class TokenCollection(Resource):
    @ns.expect(token_param)
    @ns.response(200, '{"res": True}')
    def post(self):
        """
        This is a test route
        """
        post_token = PostToken()
        return post_token.dispatch_request(request)
