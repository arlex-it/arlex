from flask import request, make_response
from flask_restplus import Resource
from Ressources.swagger_api import api
from API.User.business import get_user, create_user, delete_user
from API.User.models import user_input, user_creation
ns = api.namespace('user', description='Routes to manage users')


@ns.route('/')
class UserCollection(Resource):
    @ns.expect(user_creation)
    @ns.response(201, '{"id": 0}')
    def post(self):
        """
        Route to create an user
        """
        print("AH")
        return make_response(create_user(request))

    @ns.expect(user_input)
    @ns.response(200, '{"res": True}')
    def get(self):
        """
        Route to delete an user
        """
        return make_response(get_user(request))

@ns.route('/<int:user_id>')
@api.doc(params={'user_id': 'User ID'})
class UserCollection(Resource):
    @ns.response(202, '{"res": True}')
    def delete(self, user_id):
        """
        Route to delete an user
        :param user_id:
        :return:
        """
        print("toto")
        return make_response(delete_user(request, user_id))