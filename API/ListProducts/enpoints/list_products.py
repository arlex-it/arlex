from flask import request
from flask_restplus import Resource
from Ressources.swagger_api import api
from API.ListProducts.business import get_list_products
from API.ListProducts.models import list_products_input

ns = api.namespace('list_products', description='List the product in range of the sensor.')


@ns.route('/')
class ListProductsCollection(Resource):
    @ns.response(200, '{"products": ["product1", "product2"]}')
    def get(self):
        """
        This route list the products in range of the sensor.
        """
        return get_list_products(request)
