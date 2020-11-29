import unittest

from unit_test.init_unit_test import UnitTestInit
from unit_test.sensor.sql.sql_put import *
from unit_test.Utility.sql.oauth import UtilityOauthSQL
import requests
import socket
import json


class SensorRoutePut(unittest.TestCase):
    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    sql = PutSql(engine=engine, session=session)
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

    def test_rename_sensor(self):
        print('>>> test_rename_sensor')
        token = self.oauth_sql.create_default_access_token(id_user=self.user_id)
        data = {'old_name': 'cuisine', 'new_name': 'bureau'}
        resp = requests.put(self.public_url + '/api/sensor/update/name', headers={'Authorization': 'Bearer ' + token['token']}, json=data)
        self.oauth_sql.delete_default_access_token(self.user_id)
        self.assertEqual(202, resp.status_code)
        self.assertEqual(json.loads(resp.text)['state'], 'Le nouveau nom du capteur: cuisine, est maintenant: bureau')

    def test_sensor_not_found(self):
        print('>>> test_sensor_not_found')
        token = self.oauth_sql.create_default_access_token(id_user=self.user_id)
        data = {'old_name': 'inconnu', 'new_name': 'bureau'}
        resp = requests.put(self.public_url + '/api/sensor/update/name', headers={'Authorization': 'Bearer ' + token['token']}, json=data)
        self.oauth_sql.delete_default_access_token(self.user_id)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(json.loads(resp.text)['state'], 'Le capteur: inconnu, n\'a pas été trouvé. Veuillez réessayer.')

    def test_rename_no_data(self):
        print('>>> test_rename_no_data')
        token = self.oauth_sql.create_default_access_token(id_user=self.user_id)
        resp = requests.put(self.public_url + '/api/sensor/update/name', headers={'Authorization': 'Bearer ' + token['token']})
        self.oauth_sql.delete_default_access_token(self.user_id)
        self.assertEqual(400, resp.status_code)
        self.assertEqual(json.loads(resp.text)['state'], 'Il manque des informations pour renommer le capteur')

    def test_rename_sensor_wrong_token(self):
        print('>>> test_rename_sensor_wrong_token')
        data = {'old_name': 'inconnu', 'new_name': 'bureau'}
        resp = requests.put(self.public_url + '/api/sensor/update/name', headers={'Authorization': 'Bearer ' + 'dsgqh657dshj'}, json=data)
        self.assertEqual(500, resp.status_code)

    def test_rename_sensor_no_auth(self):
        print('>>> test_rename_sensor_no_auth')
        data = {'old_name': 'inconnu', 'new_name': 'bureau'}
        resp = requests.put(self.public_url + '/api/sensor/update/name', json=data)
        self.assertEqual(500, resp.status_code)


if __name__ == '__main__':
    unittest.main()
