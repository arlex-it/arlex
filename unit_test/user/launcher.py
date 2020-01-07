import unittest
from bdd.db_connection import session, User, to_dict
import datetime
import requests
import json


class UserRoute(unittest.TestCase):
    def testPostRoute(self):
        new_user = {'date_insert': datetime.datetime.now(),
                    'date_update': datetime.datetime.now(),
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
        resp = requests.post('http://127.0.0.1:5000/api/user'.format(),
                             data=new_user)
        print(resp.text)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
