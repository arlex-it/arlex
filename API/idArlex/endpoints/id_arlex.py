from flask import request
from flask_restplus import Resource
from Ressources.swagger_api import api
from API.idArlex.business import post_id_arlex
from API.idArlex.models import id_arlex_input

ns = api.namespace('id_arlex', description='')


@ns.route('/')
class idArlexCollection(Resource):
    @ns.expect(id_arlex_input)
    @ns.response(200, '{"res": True}')
    def post(self):
        """
        This is a test route
        """
        return post_id_arlex(request)
