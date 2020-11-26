from flask import request
from flask_restplus import Resource
from Ressources.swagger_api import api
from API.Products.models import product_update_header
from API.Allergen.business import ProductAllergenes
from API.Utilities.HttpRequest import HttpRequest

ns = api.namespace('allergen', description='route to handle allergens')


@ns.route('/<string:product_name>')
@ns.doc(params={'product_name': 'Product Name'})
class ProductAllergenesCollection(Resource):
    @ns.expect(product_update_header)
    @ns.response(200, "{'state': 'Les allergènes de ce produit sont {liste_des_allergènes}'}")
    def get(self, product_name):
        """
        Route to get allergens of a product
        """
        return ProductAllergenes(HttpRequest().get_header("Authorization")).get_product_allergenes(product_name)