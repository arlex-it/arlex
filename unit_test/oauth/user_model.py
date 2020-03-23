import datetime
from bdd.db_connection import User


def get_user_model(param=None):
    user = {'date_insert': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'date_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'is_active': 0,
            'status': 0,
            'gender': 0,
            'lastname': 'Doe',
            'firstname': 'John',
            'mail': 'john@doe.com',
            'password': '$2y$12$Egy/Ye1Ikuy4oueV9ja7T.o3eDUvGFGO4ZgdQ2VSnbjvFOz29d7zK',
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
