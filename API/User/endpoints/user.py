from flask import request, make_response
from flask_restplus import Resource
from Ressources.swagger_api import api
from API.User.business import get_user, create_user, update_user, delete_user
from API.User.models import user_get, user_input, user_creation, user_update, user_update_header

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
@ns.doc(params={'user_id': 'User ID'})
class UserCollection(Resource):
    @ns.expect(user_update, user_update_header)
    @ns.response(202, '{"res": True}')
    def put(self, user_id):
        """
        Route to update an user
        """
        return make_response(update_user(request, user_id))

    @ns.response(202, '{"res": True}')
    def delete(self, user_id):
        """
        Route to delete an user
        :param user_id:
        :return:
        """
        return make_response(delete_user(request, user_id))