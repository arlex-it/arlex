from flask import request
from flask_restplus import Resource
from API.Sensor.models import *
from API.Sensor.business import SensorBusiness
from API.Utilities.HttpRequest import HttpRequest

ns = api.namespace('sensor', description='Interagit avec les capteurs')


@ns.route('/')
class SensorCollection(Resource):
    @ns.expect(sensor_get_list_product)
    @ns.response(200, "{'state': Dans votre armoire il y a : product1, product2}")
    def get(self):
        """
        Get list of products from sensors
        """
        return SensorBusiness(HttpRequest().get_header("Authorization")).get_list_of_product(request)

    @ns.expect(sensor_post_product)
    @ns.response(200, "{'state': 'Vous avez ajouté: product1, product2'}")
    def post(self):
        """
        Link new products to a users
        """
        return SensorBusiness(HttpRequest().get_header("Authorization")).post_products(request)


@ns.route('/product/')
class ProductSensorCollection(Resource):
    @ns.expect(sensor_get_position)
    @ns.response(200, "{'state': 'Nous avons trouvé: product_name, dans: position'}")
    def get(self):
        """
        Get product position
        """
        return SensorBusiness(HttpRequest().get_header("Authorization")).get_product_position(request)


@ns.route('/update/<path:subpath>')
class SensorCollection(Resource):
    @ns.expect(sensor_rename)
    @ns.response(200, "{'state': 'Le nouveau nom du capteur: old_name, est maintenant: new_name'}")
    def put(self, subpath):
        """
        Change sensor name
        """
        if subpath.lower() == "name".lower():
            return SensorBusiness(HttpRequest().get_header("Authorization")).change_name(request)


@ns.route('/link_sensor/<int:id_sensor>/<int:id_user>')
class LinkSensorCollection(Resource):
    @ns.expect(link_sensor_post)
    @ns.response(201, "Sensor lié avec succès")
    def post(self, id_sensor, id_user):
        """
        Link a sensor to a user only if this sensor does not exist
        """
        return SensorBusiness(HttpRequest().get_header("Authorization")).link_sensor_user(request, id_sensor, id_user)


@ns.route('/link_sensor/<int:id_sensor>/<string:name>')
class LinkSensorCollection(Resource):
    @ns.expect(name_sensor)
    @ns.response(201, "Nom du sensor modifié avec succès")
    def post(self, id_sensor, name):
        """
        Name a sensor if it is already link to a user
        """
        return SensorBusiness(HttpRequest().get_header("Authorization")).name_sensor(request, id_sensor, name)


@ns.route('/list/name')
class SensorCollection(Resource):
    @ns.expect(sensor_list)
    @ns.response(201, "{'state': 'Voici la liste des endroits où je peux trouver des produits : sensor1, sensor2'}")
    def get(self):
        """
        List all user's sensors
        """
        return SensorBusiness(HttpRequest().get_header("Authorization")).get_list_name(request)
