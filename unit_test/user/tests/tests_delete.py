import unittest
import requests
from unit_test.user.user_model import get_user_model
from unit_test.init_unit_test import UnitTestInit
from unit_test.user.sql.sql_post import *
import socket


class UserRouteDelete(unittest.TestCase):
    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    sql = PostSql(engine=engine, session=session)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    public_url = "http://" + "localhost" + ":5000"
    s.close()

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
