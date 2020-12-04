from flask import request
from flask_restplus import Resource
from Ressources.swagger_api import api
from API.idArlex.business import post_id_arlex
from API.idArlex.models import id_arlex_input

ns = api.namespace('id_arlex', description='')


@ns.route('/')
class IdArlexCollection(Resource):
    @ns.expect(id_arlex_input)
    @ns.response(200, '''"id_arlex": {
    "id": "1",
    "patch_id": "15151-AZDAZD-515451",
    "product_id": "None"
  }''')
    def post(self):
        """
        Route to create id arlex
        """
        return post_id_arlex(request)
