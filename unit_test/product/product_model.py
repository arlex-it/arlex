import datetime
from bdd.db_connection import Product


def get_product_model(param=None):
    product = {
        'date_insert': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'date_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 0,
        'id_user': 1,
        "expiration_date": "2019-11-30",
        "id_rfid": 123,
        "id_ean": "3017620424403",
        "position": "placard sous evier"
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
        if key is 'id_rfid':
            new_product_object.id_rfid = product[key]
        if key is 'position':
            new_product_object.position = product[key]
        if key is 'id_user':
            new_product_object.id_user = product[key]

    return new_product_object
