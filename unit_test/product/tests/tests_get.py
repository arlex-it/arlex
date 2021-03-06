import unittest
from unit_test.product.product_model import get_product_model
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

    def tearDown(self):
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

if __name__ == '__main__':
    unittest.main()
