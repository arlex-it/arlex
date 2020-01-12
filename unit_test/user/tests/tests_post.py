import unittest
import datetime
import requests


class UserRoute(unittest.TestCase):
    def testPostRoute(self, public_url=None):
        new_user = {'date_insert': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
        resp = requests.post(public_url + '/api/user'.format(), json=new_user)
        self.assertEqual(200, resp.status_code)
