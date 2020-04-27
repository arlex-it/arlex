from flask import request
from flask_restplus import Resource
from Ressources.swagger_api import api
from API.Sensor.models import sensor_input
from API.Sensor.business import get_list_of_product

ns = api.namespace('sensor', description='Interagit avec les capteurs')


@ns.route('/<int:id>')
@ns.doc(params={'id': 'id'})
class SensorCollection(Resource):
    # @ns.expect(sensor_input)
    # @ns.response(201, '{"success": "Produit ajouté avec succès", "extra":{"id":1}}')
    def get(self, id):
        return get_list_of_product(request)
