from flask import request
from flask_restplus import Resource
from Ressources.swagger_api import api
from API.Sensor.models import sensor_input
from API.Sensor.business import SensorBusiness
from API.Utilities.HttpRequest import HttpRequest

ns = api.namespace('sensor', description='Interagit avec les capteurs')


@ns.route('/')
class SensorCollection(Resource):
    # @ns.expect(sensor_input)
    # @ns.response(201, '{"success": "Produit ajouté avec succès", "extra":{"id":1}}')
    def get(self):
        return SensorBusiness().get_list_of_product(HttpRequest().get_header("Authorization"))

    def post(self):
        return SensorBusiness.post_products(HttpRequest().get_header("Authorization"))
