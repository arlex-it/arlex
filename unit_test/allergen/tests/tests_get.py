import unittest

from unit_test.allergen.allergen_model import get_user_model
from unit_test.init_unit_test import UnitTestInit
from unit_test.allergen.sql.sql_post import *
from unit_test.Utility.sql.oauth import UtilityOauthSQL
import requests
import socket
import json


class AllergenRouteGet(unittest.TestCase):
    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    sql = PostSql(engine=engine, session=session)
    oauth_sql = UtilityOauthSQL(engine=engine, session=session)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    public_url = "http://localhost:5000"
    s.close()
    user_id = sql.create_user(user=get_user_model())
    product_id = sql.create_product(product=get_product_model({'id_user': user_id}))

    def test_get_allergen(self):
        print('>>> test_get_allergen')
        token = self.oauth_sql.create_default_access_token(id_user=self.user_id)
        resp = requests.get(self.public_url + '/api/allergen/Nutella', headers={'Authorization': 'Bearer ' + token['token']})
        self.oauth_sql.delete_default_access_token(self.user_id)
        self.assertEqual(200, resp.status_code)

    def test_get_allergen_altered_product(self):
        print('>>> test_get_allergen_altered_product')
        token = self.oauth_sql.create_default_access_token(id_user=self.user_id)
        resp = requests.get(self.public_url + '/api/allergen/Nutola', headers={'Authorization': 'Bearer ' + token['token']})
        self.oauth_sql.delete_default_access_token(self.user_id)
        self.assertEqual(200, resp.status_code)

    def test_get_allergen_product_not_associated(self):
        print('>>> test_get_allergen_product_not_associated')
        token = self.oauth_sql.create_default_access_token(id_user=self.user_id)
        resp = requests.get(self.public_url + '/api/allergen/Farine', headers={'Authorization': 'Bearer ' + token['token']})
        self.oauth_sql.delete_default_access_token(self.user_id)
        self.assertEqual(json.loads(resp.text)['state'], 'Nous n\'avons pas trouvé de produit enregistré sur votre compte.')
        self.assertEqual(200, resp.status_code)

    def test_get_allergen_wrong_token(self):
        print('>>> test_get_allergen_wrong_token')
        resp = requests.get(self.public_url + '/api/allergen/Nutella', headers={'Authorization': 'Bearer ' + 'dhsqui73dsq'})
        self.oauth_sql.delete_default_access_token(self.user_id)
        self.assertEqual(500, resp.status_code)

    def test_get_allergen_no_auth(self):
        print('>>> test_get_allergen_no_auth')
        resp = requests.get(self.public_url + '/api/allergen/Nutella')
        self.oauth_sql.delete_default_access_token(self.user_id)
        self.assertEqual(500, resp.status_code)

    sql.delete_product_by_id(product_id)
    sql.delete_user_by_id(user_id)


if __name__ == '__main__':
    unittest.main()
