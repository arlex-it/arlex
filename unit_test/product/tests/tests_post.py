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
        new_product = get_product_model()
        resp = requests.post(self.public_url + '/api/product'.format(), json=new_product)
        self.assertEqual(201, resp.status_code)

        # try to create a bad product
        create_product(self.engine)
        new_product = get_product_model()
        resp = requests.post(self.public_url + '/api/product'.format(), json=new_product)
        self.assertEqual(403, resp.status_code)
