import unittest
from unit_test.product.product_model import get_product_model
from unit_test.init_unit_test import UnitTestInit
from unit_test.product.sql.sql_post import *
import requests

import time


class ProductsRouteGet(unittest.TestCase):

    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    public_url = unit_test_init.create_tunnel()
    sql = PostSql(engine=engine, session=session)

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
        time.sleep(0.5)

    def test_get_wrong_product(self):
        print(">>> test_get_wrong_product")
        resp = requests.get(self.public_url + '/api/products/{}'.format(1000))
        self.assertEqual(resp.status_code, 403)
        time.sleep(0.5)


if __name__ == '__main__':
    unittest.main()
