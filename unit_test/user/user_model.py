import datetime


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
