import datetime
from bdd.db_connection import User, Sensor


def get_user_model(param=None):
    user = {'date_insert': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'date_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'is_active': 0,
            'status': 0,
            'gender': 0,
            'lastname': 'Doe',
            'firstname': 'John',
            'mail': 'john@doe.com',
            'password': 'password',
            'country': 'France',
            'town': 'Lille',
            'street': 'rue nationale',
            'street_number': '13',
            'region': 'Hauts de france',
            'postal_code': '59000'}
    if param:
        for key in param:
            if key in user:
                user[key] = param[key]
    return user


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


def get_sensor_model(param=None):
    product = {
        'date_insert': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'date_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'is_active': 1,
        'id_user': 1,
        'type': 0,
        'name': 'cuisine',
        'sensorcol': '0'
    }
    if param:
        for key in param:
            if key in product:
                product[key] = param[key]
    return product


def sensor_model_to_sql(sensor):
    new_sensor_object = Sensor()
    for key in sensor:
        if key is 'date_insert':
            new_sensor_object.date_insert = sensor[key]
        if key is 'date_update':
            new_sensor_object.date_update = sensor[key]
        if key is 'is_active':
            new_sensor_object.is_active = sensor[key]
        if key is 'id_user':
            new_sensor_object.id_user = sensor[key]
        if key is 'type':
            new_sensor_object.type = sensor[key]
        if key is 'name':
            new_sensor_object.name = sensor[key]
        if key is 'sensorcol':
            new_sensor_object.sensorcol = sensor[key]

    return new_sensor_object
