from flask import request
from flask_restplus import Resource

from Ressources.swagger_api import api
from API.Token.business import PostToken
from API.Token.models import token_param

ns = api.namespace('token', description='mange token')


@ns.route('/')
class TokenCollection(Resource):
    @ns.expect(token_param)
    @ns.response(200, '{token data}')
    def post(self):
        """
        Route to handle tokens
        """
        post_token = PostToken()
        return post_token.dispatch_request(request)
