import unittest
import requests
from unit_test.user.user_model import get_user_model
from unit_test.user.sql.sql_post import *
from unit_test.init_unit_test import UnitTestInit


class UserRoute(unittest.TestCase):

    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    public_url = unit_test_init.create_tunnel()
    sql = PostSql(engine=engine, session=session)

    def test_create_user(self):
        # create user
        new_user = get_user_model()
        resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
        self.assertEqual(201, resp.status_code)
        self.sql.delete_all_user()

    def test_user_already_exist(self):
        # try to create user with existing email
        new_user = get_user_model()
        self.sql.create_user(user=new_user)
        resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
        self.assertEqual(403, resp.status_code)
        self.sql.delete_all_user()


if __name__ == '__main__':
    unittest.main()
