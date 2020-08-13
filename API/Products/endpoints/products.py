from flask import request
from flask_restplus import Resource
from Ressources.swagger_api import api
from API.Products.business import post_product, delete_products, get_products, ProductIngredients
from API.Products.models import products_create, product_authorization_header, product_update_header
from API.Utilities.HttpRequest import HttpRequest

ns = api.namespace('products', description='Routes des produits.')


@ns.route('/')
class ProductsCollection(Resource):
    @ns.expect(products_create)
    @ns.response(201, '{"success": "Produit ajouté avec succès", "extra":{"id":1}}')
    def post(self):
        """
        This is a test route
        """
        return post_product(request)


@ns.route('/<int:product_id>')
@ns.doc(params={'product_id': 'Product ID'})
class UpdateProductCollection(Resource):
    @ns.response(201, '{"success": "Produit supprimé avec succès"}')
    def delete(self, product_id):
        """
        Route to delete a product
        :param product_id:
        :return:
        """
        return delete_products(request, product_id)

    def get(self, product_id):
        """
        Route to get product infos
        :param product_id:
        :return:
        """
        return get_products(request, product_id)


@ns.route('/ingredients/<string:product_name>')
@ns.doc(params={'product_name': 'Product Name'})
class ProductIngredientsCollection(Resource):
    @ns.expect(product_authorization_header)
    def get(self, product_name):
        return ProductIngredients(HttpRequest().get_header("Authorization")).get_product_ingredients(product_name)
