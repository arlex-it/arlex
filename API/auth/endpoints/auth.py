from flask import request
from flask_restplus import Resource
from Ressources.swagger_api import api
from API.auth.business import get_auth, post_token
from API.auth.models import auth_input

ns = api.namespace('auth', description='Routes authentifications')


@ns.route('/authorize')
class authCollection(Resource):
    @ns.expect(auth_input)
    @ns.response(200, '{"res": True}')
    def get(self):
        """
        This is a to get authorize
        """
        return get_auth(request)

    @ns.expect(auth_input)
    @ns.response(200, '{"res": True}')
    def post(self):
        """
        This is a to get authorize
        """
        return post_token(request)