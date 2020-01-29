import unittest
from unit_test.user.user_model import get_user_model
from unit_test.init_unit_test import UnitTestInit
from unit_test.user.sql.sql_post import *
import requests


class MyTestCase(unittest.TestCase):

    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    public_url = unit_test_init.create_tunnel()
    sql = PostSql(engine=engine, session=session)

    def tearDown(self):
        self.sql.delete_all_user()

    def test_delete_user(self):
        print(">>> test_delete_user")
        new_user = get_user_model()
        user_id = self.sql.create_user(user=new_user)
        resp = requests.delete(self.public_url + '/api/user/{}'.format(user_id))
        self.assertEqual(resp.status_code, 202)
        self.assertIsNone(self.sql.get_user_by_id(user_id))

    def test_delete_wrong_user(self):
        print(">>> test_delete_wrong_user")
        resp = requests.delete(self.public_url + '/api/user/{}'.format(1000))
        self.assertEqual(resp.status_code, 403)


if __name__ == '__main__':
    unittest.main()
