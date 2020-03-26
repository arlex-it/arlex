from flask import request
from flask_restplus import Resource

from API.Utilities.auth import require_authentication
from Ressources.swagger_api import api
from API.auth.GetAuthorizationBuisness import GetAuthorization
from API.auth.PostAuthorizationBuisness import PostAuthorization
from API.auth.models import auth_input, auth_authorize_param

ns = api.namespace('auth', description='Routes authentifications')


@ns.route('/authorize')
class authCollection(Resource):
    @ns.expect(auth_authorize_param)
    @ns.response(200, '{"res": True}')
    def get(self):
        """
        This is a to get authorize
        """
        get_auth = GetAuthorization()
        return get_auth.dispatch_request(request)

    def post(self):
        """
        Post authorize (called after get)
        :return:
        """
        post_auth = PostAuthorization()
        return post_auth.dispatch_request(request)
