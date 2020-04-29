import unittest
import requests
from unit_test.user.user_model import get_user_model
from unit_test.init_unit_test import UnitTestInit
from unit_test.user.sql.sql_post import *
from unit_test.Utility.sql.oauth import UtilityOauthSQL
import socket


class UserRouteDelete(unittest.TestCase):
    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    sql = PostSql(engine=engine, session=session)
    oauth_sql = UtilityOauthSQL(engine=engine, session= session)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    public_url = "http://" + "localhost" + ":5000"
    s.close()

    def tearDown(self):
        self.sql.delete_all_user()

    def test_delete_user(self):
        print(">>> test_delete_user")
        new_user = get_user_model()
        id_user = self.sql.create_user(user=new_user)

        # create user token
        token = self.oauth_sql.create_default_access_token(id_user=id_user)

        resp = requests.delete(self.public_url + '/api/user/{}'.format(id_user), headers={'Authorization': 'Bearer ' + token['token']})
        self.assertEqual(resp.status_code, 202)
        self.assertIsNone(self.sql.get_user_by_id(id_user))

    def test_delete_wrong_user(self):
        print(">>> test_delete_wrong_user")

        # create user token
        token = self.oauth_sql.create_default_access_token(id_user=1000)

        resp = requests.delete(self.public_url + '/api/user/{}'.format(1000), headers={'Authorization': 'Bearer ' + token['token']})
        self.assertEqual(resp.status_code, 403)


if __name__ == '__main__':
    unittest.main()
