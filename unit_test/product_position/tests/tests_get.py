import unittest

from unit_test.init_unit_test import UnitTestInit
from unit_test.product_position.sql.sql_post import *
from unit_test.Utility.sql.oauth import UtilityOauthSQL
import requests
import socket
import json


class ProductPositionGet(unittest.TestCase):
    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    sql = PostSql(engine=engine, session=session)
    oauth_sql = UtilityOauthSQL(engine=engine, session=session)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    public_url = "http://localhost:5000"
    s.close()

    def setUp(self):
        self.user_id = self.sql.create_user(user=get_user_model())
        self.product_id = self.sql.create_product(product=get_product_model({'id_user': self.user_id}))
        self.sensor_id = self.sql.create_sensor(sensor=get_sensor_model({'id_user': self.user_id}))

    def tearDown(self):
        self.sql.delete_product_by_id(self.product_id)
        self.sql.delete_user_by_id(self.user_id)
        self.sql.delete_sensor_by_id(self.sensor_id)

    def test_get_product_position(self):
        print('>>> test_get_product_position')
        token = self.oauth_sql.create_default_access_token(id_user=self.user_id)
        resp = requests.get(self.public_url + '/api/sensor/product?product_name=Nutella', headers={'Authorization': 'Bearer ' + token['token']})
        self.oauth_sql.delete_default_access_token(self.user_id)
        self.assertEqual(json.loads(resp.text)['state'], 'Nous avons trouvé: Nutella, dans: placard sous evier.')
        self.assertEqual(200, resp.status_code)

    def test_get_product_position_no_product_name(self):
        print('>>> test_get_product_position_no_product_name')
        token = self.oauth_sql.create_default_access_token(id_user=self.user_id)
        resp = requests.get(self.public_url + '/api/sensor/product', headers={'Authorization': 'Bearer ' + token['token']})
        self.oauth_sql.delete_default_access_token(self.user_id)
        self.assertEqual(json.loads(resp.text)['state'], 'Nous n\'avons pas pu récupérer le nom du produit demandé.')
        self.assertEqual(200, resp.status_code)

    def test_get_product_position_empty_product_name(self):
        print('>>> test_get_product_position_empty_product_name')
        token = self.oauth_sql.create_default_access_token(id_user=self.user_id)
        resp = requests.get(self.public_url + '/api/sensor/product?product_name=', headers={'Authorization': 'Bearer ' + token['token']})
        self.oauth_sql.delete_default_access_token(self.user_id)
        self.assertEqual(json.loads(resp.text)['state'], 'Nous n\'avons pas trouvé de produit correspondant à votre recherche: .')
        self.assertEqual(200, resp.status_code)

    def test_get_product_position_altered_product(self):
        print('>>> test_get_product_position_altered_product')
        token = self.oauth_sql.create_default_access_token(id_user=self.user_id)
        resp = requests.get(self.public_url + '/api/sensor/product?product_name=Nutola', headers={'Authorization': 'Bearer ' + token['token']})
        self.oauth_sql.delete_default_access_token(self.user_id)
        self.assertEqual(200, resp.status_code)

    def test_get_product_position_product_not_associated(self):
        print('>>> test_get_product_position_product_not_associated')
        token = self.oauth_sql.create_default_access_token(id_user=self.user_id)
        resp = requests.get(self.public_url + '/api/sensor/product?product_name=Farine', headers={'Authorization': 'Bearer ' + token['token']})
        self.oauth_sql.delete_default_access_token(self.user_id)
        self.assertEqual(json.loads(resp.text)['state'], 'Nous n\'avons pas trouvé de produit correspondant à votre recherche: Farine.')
        self.assertEqual(200, resp.status_code)

    def test_get_product_position_wrong_token(self):
        print('>>> test_get_product_position_wrong_token')
        resp = requests.get(self.public_url + '/api/sensor/product?product_name=Nutella', headers={'Authorization': 'Bearer ' + 'dhsqui73dsq'})
        self.oauth_sql.delete_default_access_token(self.user_id)
        self.assertEqual(500, resp.status_code)

    def test_get_product_position_no_auth(self):
        print('>>> test_get_product_position_no_auth')
        resp = requests.get(self.public_url + '/api/sensor/product?product_name=Nutella')
        self.oauth_sql.delete_default_access_token(self.user_id)
        self.assertEqual(500, resp.status_code)


if __name__ == '__main__':
    unittest.main()
