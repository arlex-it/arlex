import unittest

from unit_test.init_unit_test import UnitTestInit
from unit_test.sensor.sql.sql_put import *
from unit_test.Utility.sql.oauth import UtilityOauthSQL
import requests
import socket
import json


class SensorRoutePost(unittest.TestCase):
    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    sql = PostSql(engine=engine, session=session)
    oauth_sql = UtilityOauthSQL(engine=engine, session=session)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    public_url = "http://localhost:5000"
    s.close()
    user_id = 0
    sensor_id = 0

    def setUp(self):
        self.user_id = self.sql.create_user(user=get_user_model())
        self.sensor_id = self.sql.create_sensor(sensor=get_sensor_model({'id_user': self.user_id}))

    def tearDown(self):
        self.sql.delete_sensor_by_id(self.sensor_id)
        self.sql.delete_user_by_id(self.user_id)

    def test_post_sensor(self):
        print('>>> test_post_sensor')
        token = self.oauth_sql.create_default_access_token(id_user=self.user_id)
        resp = requests.post(self.public_url + '/api/sensor/', headers={'Authorization': 'Bearer ' + token['token']})
        self.assertEqual(200, resp.status_code)

    sql.delete_product_by_id(product_id)
    sql.delete_user_by_id(user_id)


if __name__ == '__main__':
    unittest.main()
