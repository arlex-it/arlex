import datetime
from bdd.db_connection import Product, User


def get_product_model(param=None):
    product = {
        'date_insert': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'date_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 0,
        'id_user': 1,
        "expiration_date": "2019-11-30",
        "id_arlex": "BLA-OKA-PAD",
        "id_ean": "3017620424403",
        "position": "placard sous evier",
        "product_name": "Un produit",
        "product_name_gen": "Un produit generique :D",
    }
    if param:
        for key in param:
            if key in product:
                product[key] = param[key]
    return product


def product_model_to_sql(product):
    new_product_object = Product()
    for key in product:
        if key is 'date_insert':
            new_product_object.date_insert = product[key]
        if key is 'date_update':
            new_product_object.date_update = product[key]
        if key is 'expiration_date':
            new_product_object.expiration_date = product[key]
        if key is 'status':
            new_product_object.status = product[key]
        if key is 'id_ean':
            new_product_object.id_ean = product[key]
        if key is 'id_arlex':
            new_product_object.id_rfid = product[key]
        if key is 'position':
            new_product_object.position = product[key]
        if key is 'id_user':
            new_product_object.id_user = product[key]

    return new_product_object

def user_model_to_sql(user):
    new_user_object = User()
    for key in user:
        if key is 'date_insert':
            new_user_object.date_insert = user[key]
        if key is 'date_update':
            new_user_object.date_update = user[key]
        if key is 'is_active':
            new_user_object.is_active = user[key]
        if key is 'status':
            new_user_object.status = user[key]
        if key is 'gender':
            new_user_object.gender = user[key]
        if key is 'lastname':
            new_user_object.lastname = user[key]
        if key is 'firstname':
            new_user_object.firstname = user[key]
        if key is 'mail':
            new_user_object.mail = user[key]
        if key is 'password':
            new_user_object.password = user[key]
        if key is 'country':
            new_user_object.country = user[key]
        if key is 'town':
            new_user_object.town = user[key]
        if key is 'street':
            new_user_object.street = user[key]
        if key is 'street_number':
            new_user_object.street_number = user[key]
        if key is 'region':
            new_user_object.region = user[key]
        if key is 'postal_code':
            new_user_object.postal_code = user[key]

    return new_user_object
