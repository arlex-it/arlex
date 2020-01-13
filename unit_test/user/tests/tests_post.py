import unittest
import requests
from unit_test.user.user_model import get_user_model
from unit_test.user.sql.sql_post import *


class UserRoute(unittest.TestCase):
    def __init__(self, engine=None, public_url=None):
        super().__init__()
        self.engine = engine
        self.public_url = public_url

    def testPostRoute(self):
        # create user
        new_user = get_user_model()
        resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
        self.assertEqual(201, resp.status_code)
        # TODO delete user

        # try to create user with existing email
        create_user(self.engine)
        new_user = get_user_model()
        resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
        self.assertEqual(403, resp.status_code)
        # TODO delete user
