import re
import requests

from flask import jsonify
from flask_restplus import abort

from API.Utilities.EanUtilities import EanUtilities
from API.Utilities.HttpResponse import HttpResponse
from API.Products.business import post_products
from bdd.db_connection import session, AccessToken, Product, to_dict
from API.Products.business import post_product
from API.Utilities.ErrorEnum import *


class SensorBusiness():
    def __init__(self, header_token=None):
        if not header_token:
            raise Exception("Token undefined")

        print(header_token)

        reg = re.compile('Bearer ([A-Za-z0-9-=]+)')
        result = reg.findall(header_token)

        if not result:
            raise Exception("Token undefined")

        token = result[0]
        print(token)

        user_connected = session.query(AccessToken).filter(AccessToken.token == token).first()
        users = to_dict(user_connected)
        self.user_connected = users["id_user"]
        print(self.user_connected)

    def get_list_of_product(self, request):
        print(self.user_connected)
        res = requests.get('http://35.210.200.125:5000/').json()
        print(res)

        if len(res['product_list']) == 0:
            state_res = 'Il n y a rien dans votre armoire'
        else:
            state_res = 'Dans votre armoire il y a : '
            product = ", ".join(res['product_list'])
            state_res += product

        return HttpResponse(200).custom({'state': state_res})

    def post_products(self, request):

        ean_utilities = EanUtilities()

        res = requests.get('http://35.210.200.125:5000/').json()
        print("RESSSSS", res)

        old_products_list = session.query(Product).filter(Product.id_user == self.user_connected).all()
        print(old_products_list)

        ean_list = [product.id_ean for product in old_products_list]
        print(ean_list)

        res_list = res["product_list"]
        new_elements = [item for item in res_list if item not in ean_list]

        print(new_elements)
        products_added = post_products(new_elements, self.user_connected)

        print(products_added)

        # TODO : STOCKER LA DIFF EN BDD
        #        FAIRE UNE FONCTION CONVERSION EAN VERS NOM
        #        RETOURNER LES NOMS A L'ASSISTANT VOCAL

        # for i in res:
        # create_products(i, self.user_connected)

        return HttpResponse(200).custom({'state': 'Vous avez ajouté: coca'})