from flask import request
from flask_restplus import Resource

from API.Utilities.auth import require_authentication
from Ressources.swagger_api import api
from API.auth.GetAuthorizationBuisness import GetAuthorization
from API.auth.PostAuthorizationBuisness import PostAuthorization
from API.auth.models import auth_authorize_param, post_auth_model

ns = api.namespace('auth', description='Authentication routes')


@ns.route('/authorize')
class authCollection(Resource):
    @ns.expect(auth_authorize_param)
    def get(self):
        """
        Route to get authorization
        """
        get_auth = GetAuthorization()
        return get_auth.dispatch_request(request)

    @ns.expect(post_auth_model)
    def post(self):
        """
        Route to authorize registered user or redirect to create account
        """
        post_auth = PostAuthorization()
        return post_auth.dispatch_request(request)
