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
        return SensorBusiness(HttpRequest().get_header("Authorization")).get_list_of_product(request)

    def post(self):
        return SensorBusiness(HttpRequest().get_header("Authorization")).post_products(request)


@ns.route('/product/')
class ProductSensorCollection(Resource):
    def get(self):
        return SensorBusiness(HttpRequest().get_header("Authorization")).get_product_position(request)


@ns.route('/update/<path:subpath>')
class SensorCollection(Resource):
    def put(self, subpath):
        if subpath.lower() == "name".lower():
            return SensorBusiness(HttpRequest().get_header("Authorization")).change_name(request)


@ns.route('/link_sensor/<int:id_sensor>/<int:id_user>')
class LinkSensorCollection(Resource):
    def post(self, id_sensor, id_user):
        return SensorBusiness(HttpRequest().get_header("Authorization")).link_sensor_user(request, id_sensor,
                                                                                          id_user)

@ns.route('/link_sensor/<int:id_sensor>/<string:name>')
class LinkSensorCollection(Resource):
    def post(self, id_sensor, name):
        return SensorBusiness(HttpRequest().get_header("Authorization")).name_sensor(request, id_sensor, name)


@ns.route('/list/name')
class SensorCollection(Resource):
    def get(self):
        return SensorBusiness(HttpRequest().get_header("Authorization")).get_list_name(request)
