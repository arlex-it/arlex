import unittest
import datetime
import requests
from unit_test.user.user_model import get_user_model


class UserRoute(unittest.TestCase):
    def testPostRoute(self, public_url=None):
        # create user
        new_user = get_user_model()
        resp = requests.post(public_url + '/api/user'.format(), json=new_user)
        self.assertEqual(201, resp.status_code)

        # try to create user with existing email
        resp = requests.post(public_url + '/api/user'.format(), json=new_user)
        self.assertEqual(403, resp.status_code)
