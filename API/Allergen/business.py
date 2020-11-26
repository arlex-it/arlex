import re
import json

from API.Utilities.OpenFoodFactsUtilities import OpenFoodFactsUtilities
from API.Utilities.EanUtilities import EanUtilities
from bdd.db_connection import session, Product, to_dict, IdArlex, AccessToken
from API.Utilities.HttpResponse import *


class ProductAllergenes:
    def __init__(self, header_token=None):
        if not header_token:
            print("no token")
            raise Exception("Token undefined")

        reg = re.compile('Bearer ([A-Za-z0-9-=]+)')
        result = reg.findall(header_token)

        if not result:
            raise Exception("Token undefined")

        token = result[0]

        user_connected = session.query(AccessToken).filter(AccessToken.token == token).first()
        users = to_dict(user_connected)
        self.user_connected = users["id_user"]

    def get_product_allergenes(self, product_name):
        products_list = session.query(Product).filter(Product.id_user == self.user_connected).all()
        # search product by name in product's user list
        ean_list = EanUtilities().search_product(products_list, product_name)
        if not ean_list:
            return HttpResponse(200).custom({'state': 'Nous n\'avons pas trouvé de produit enregistré sur votre compte.'})
        # get best result of products found and get product's infos via openfoodfacts
        ean_list = ean_list[0]
        product = OpenFoodFactsUtilities().get_open_request_cache('https://world.openfoodfacts.org/api/v0/product/' + ean_list['id_ean'])
        if type(product) is str:
            product = json.loads(product)
        if 'allergens_from_ingredients' not in product['product'] or ('allergens_hierarchy' in product['product'] and len(product['product']['allergens_hierarchy']) == 0):
            # no allergen found
            return HttpResponse(200).custom({'state': 'Nous n\'avons pas trouvé d\'allergène.'})
        elif 'allergens_from_ingredients' not in product['product']:
            # don't know if there is allergen
            return HttpResponse(200).custom({'state': 'Nous n\'avons pas pu déterminer les allergènes.'})
        return HttpResponse(200).custom({'state': f"Les allergènes de ce produit sont {product['product']['allergens_from_ingredients']}"})