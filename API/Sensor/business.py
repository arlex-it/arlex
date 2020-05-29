import re
import requests

from flask import jsonify
from flask_restplus import abort

from API.Utilities.EanUtilities import EanUtilities
from API.Utilities.HttpResponse import HttpResponse
from API.Products.business import post_products, link_product_to_user_with_id_rfid, get_product_name_with_rfid
from bdd.db_connection import session, AccessToken, Product, to_dict
from API.Utilities.OpenFoodFactsUtilities import OpenFoodFactsUtilities
from API.Products.business import post_product
from API.Utilities.ErrorEnum import *


class SensorBusiness():
    def __init__(self, header_token=None):
        if not header_token:
            raise Exception("Token undefined")


        reg = re.compile('Bearer ([A-Za-z0-9-=]+)')
        result = reg.findall(header_token)

        if not result:
            raise Exception("Token undefined")

        token = result[0]

        user_connected = session.query(AccessToken).filter(AccessToken.token == token).first()
        users = to_dict(user_connected)
        self.user_connected = users["id_user"]

    def get_list_of_product(self, request):
        res = requests.get('http://35.210.200.125:5000/').json()

        if len(res['product_list']) == 0:
            state_res = 'Il n y a rien dans votre armoire'
        else:
            name_new_element = []
            for element in res['product_list']:
                name_new_element.append(get_product_name_with_rfid(element))
            state_res = 'Dans votre armoire il y a : '
            product = ", ".join(name_new_element)
            state_res += product

        return HttpResponse(200).custom({'state': state_res})

    def post_products(self, request):

        res = requests.get('http://35.210.200.125:5000/').json()

        old_products_list = session.query(Product).filter(Product.id_user == self.user_connected).all()

        id_rfid_list = [product.id_rfid for product in old_products_list]

        converted_list = [str(i) for i in id_rfid_list]
        res_list = res["product_list"]
        new_elements = [item for item in res_list if item not in converted_list]
        if len(new_elements) == 0:
            return HttpResponse(200).custom({'state': "J'ai déjà enregistrer tout les produits dans votre armoire."})

        name_new_element = []
        for element in new_elements:
            link_product_to_user_with_id_rfid(element, self.user_connected)
            name_new_element.append(get_product_name_with_rfid(element))


        name_to_return = ', '.join(name_new_element)
        return HttpResponse(200).custom({'state': f'Vous avez ajouté: {name_to_return}'})