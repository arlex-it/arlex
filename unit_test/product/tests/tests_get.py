import unittest
from unit_test.product.product_model import get_product_model, get_user_model
from unit_test.init_unit_test import UnitTestInit
from unit_test.product.sql.sql_post import *
import requests
import socket


class ProductsRouteGet(unittest.TestCase):
    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    sql = PostSql(engine=engine, session=session)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    public_url = "http://localhost:5000"
    s.close()

    user_id = 0

    def setUp(self):
        self.user_id = self.sql.create_user(user=get_user_model())

    def tearDown(self):
        self.sql.delete_user_by_id(self.user_id)
        self.sql.delete_all_product()

    def test_get_product(self):
        print(">>> test_get_product")
        new_product = get_product_model()
        product_id = self.sql.create_product(product=new_product)
        resp = requests.get(self.public_url + '/api/products/{}'.format(product_id))
        self.assertEqual(resp.status_code, 200)
        product = self.sql.get_product_by_id(product_id)
        self.assertEqual(product['expiration_date'].strftime("%Y-%m-%d"), new_product['expiration_date'])
        self.assertEqual(product['id_ean'], new_product['id_ean'])
        self.assertEqual(product['position'], new_product['position'])

    def test_get_wrong_product(self):
        print(">>> test_get_wrong_product")
        resp = requests.get(self.public_url + '/api/products/{}'.format(1000))
        self.assertEqual(resp.status_code, 403)

    def test_get_product_ingredients(self):
        print(">>> test_get_product_ingredients")
        token = self.oauth_sql.create_default_access_token(id_user=self.user_id)
        new_product = get_product_model()
        product_name = self.sql.create_product_with_name(product=new_product)
        resp = requests.get(self.public_url + '/api/products/ingredients/{}'.format(product_name),
                            headers={'Authorization': 'Bearer ' + token['token']})
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
