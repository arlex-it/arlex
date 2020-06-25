from flask import request
from flask_restplus import Resource
from Ressources.swagger_api import api
from API.Products.business import post_product, delete_products, get_products
from API.Products.models import products_create

ns = api.namespace('products', description='Routes des produits')


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
