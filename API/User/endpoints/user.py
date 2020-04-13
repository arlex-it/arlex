from flask import request
from flask_restplus import Resource

from API.Utilities.auth import require_authentication
from Ressources.swagger_api import api
from API.User.business import get_user, create_user, update_user, delete_user
from API.User.models import user_get, user_creation, user_update, user_update_header

ns = api.namespace('user', description='Routes to manage users')


@ns.route('/')
class UserCollection(Resource):
    @ns.expect(user_creation)
    @ns.response(201, '{"success": "Utilisateur créé avec succès", "extra":{"id": 1}')
    def post(self):
        """
        Route to create an user
        """
        return create_user(request)

    @ns.expect(user_get)
    @ns.response(200, '{"res": True}')
    def get(self):
        """
        Route to get an user (dev only for the moment)
        """
        return get_user(request)


@ns.route('/<int:user_id>')
@ns.doc(params={'user_id': 'User ID'})
class UpdateUserCollection(Resource):
    @ns.expect(user_update, user_update_header)
    @ns.response(200, '{"success": "Utilisateur modifié avec succès."}')
    @require_authentication('private')
    def put(self, user_id):
        """
        Route to update an user
        """
        return update_user(request, user_id)

    @ns.response(202, '{"success": "Utilisateur supprimé avec succès."}')
    @require_authentication('private')
    def delete(self, user_id):
        """
        Route to delete an user
        :param user_id:
        :return:
        """
        return delete_user(request, user_id)
