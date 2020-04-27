import unittest
from unit_test.product.product_model import get_product_model
from unit_test.init_unit_test import UnitTestInit
from unit_test.product.sql.sql_post import *
import requests
import socket


class ProductsRouteDelete(unittest.TestCase):

    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    sql = PostSql(engine=engine, session=session)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    public_url = "http://" + "localhost" + ":5000"
    s.close()

    def tearDown(self):
        self.sql.delete_all_product()

    def test_delete_product(self):
        print(">>> test_delete_product")
        new_product = get_product_model()
        product_id = self.sql.create_product(product=new_product)
        resp = requests.delete(self.public_url + '/api/products/{}'.format(product_id))
        self.assertEqual(resp.status_code, 202)
        product = self.sql.get_product_by_id(product_id)
        self.assertEqual(product, None)

    def test_delete_wrong_product(self):
        print(">>> test_delete_wrong_product")
        resp = requests.delete(self.public_url + '/api/products/{}'.format(1000))
        self.assertEqual(resp.status_code, 403)

if __name__ == '__main__':
    unittest.main()
