import unittest
import requests
from unit_test.product.product_model import get_product_model
from unit_test.product.sql.sql_post import *


class ProductRoute(unittest.TestCase):
    def __init__(self, engine=None, public_url=None):
        super().__init__()
        self.engine = engine
        self.public_url = public_url

    def testPostRoute(self):
        # create product
        delete_all_products(self.engine)
        new_product = get_product_model()
        resp = requests.post(self.public_url + '/api/products'.format(), json=new_product)
        self.assertEqual(201, resp.status_code)

        # try to create a bad product
        new_product = get_product_model()
        new_product.pop('id_ean', None)
        resp = requests.post(self.public_url + '/api/products'.format(), json=new_product)
        self.assertEqual(400, resp.status_code)

    def testGetRoute(self):
        print("~~~~~~ Get Route  ~~~~~~")
        delete_all_products(self.engine)
        prod_id = create_product(self.engine)
        resp = requests.get(self.public_url + '/api/products/{}'.format(prod_id))
        # print(resp.json())
        self.assertEqual(200, resp.status_code)
        print("Real Product find : OK")
        delete_all_products(self.engine)
        resp = requests.get(self.public_url + '/api/products/0'.format())
        self.assertEqual(403, resp.status_code)
        print("Fake Product failed : OK")

    def testDeleteRoute(self):
        return