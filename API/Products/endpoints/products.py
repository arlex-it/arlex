from flask import request
from flask_restplus import Resource
from Ressources.swagger_api import api
from API.Products.business import get_products
from API.Products.models import products_input

ns = api.namespace('products', description='Routes des produits')


@ns.route('/')
class ProductsCollection(Resource):
    @ns.expect(products_input)
    @ns.response(200, '{"res": True}')
    def post(self):
        """
        This is a test route
        """
        return get_products(request)
