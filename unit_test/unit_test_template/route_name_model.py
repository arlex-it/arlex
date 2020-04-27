import datetime
#from bdd.db_connection import Model_name

"""
/!\ DO NOT forget to rename functions and variables /!\ 
"""


def get_model(param=None):
    model = {
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
            if key in model:
                model[key] = param[key]
    return model


def model_to_sql(model):
    new_object = model()
    for key in model:
        if key is 'date_insert':
            new_object.date_insert = model[key]
        if key is 'date_update':
            new_object.date_update = model[key]
        if key is 'expiration_date':
            new_object.expiration_date = model[key]
        if key is 'status':
            new_object.status = model[key]
        if key is 'id_ean':
            new_object.id_ean = model[key]
        if key is 'id_rfid':
            new_object.id_rfid = model[key]
        if key is 'position':
            new_object.position = model[key]
        if key is 'id_user':
            new_object.id_user = model[key]

    return new_object
