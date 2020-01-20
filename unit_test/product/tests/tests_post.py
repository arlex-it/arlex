# import unittest
# import requests
# from unit_test.product.product_model import get_product_model
# from unit_test.product.sql.sql_post import *
# 
# 
# class ProductRoute(unittest.TestCase):
#     def __init__(self, engine=None, public_url=None):
#         super().__init__()
#         self.engine = engine
#         self.public_url = public_url
# 
#     def testPostRoute(self):
#         # create product
#         delete_all_products(self.engine)
#         new_product = get_product_model()
#         resp = requests.post(self.public_url + '/api/productss'.format(), json=new_product)
#         self.assertEqual(201, resp.status_code)
# 
#         # try to create a bad product
#         new_product = get_product_model()
#         new_product.pop('id_ean', None)
#         resp = requests.post(self.public_url + '/api/productss'.format(), json=new_product)
#         self.assertEqual(400, resp.status_code)
# 
#     def testGetRoute(self):
#         print("~~~~~~ Get Route  ~~~~~~")
#         delete_all_products(self.engine)
#         prod_id = create_product(self.engine)
#         resp = requests.get(self.public_url + '/api/productss/{}'.format(prod_id))
#         # print(resp.json())
#         self.assertEqual(200, resp.status_code)
#         print("Real Product find : OK")
#         delete_all_products(self.engine)
#         resp = requests.get(self.public_url + '/api/productss/0'.format())
#         self.assertEqual(403, resp.status_code)
#         print("Fake Product failed : OK")
# 
#     def testDeleteRoute(self):
#         return

import unittest

import requests

from unit_test.init_unit_test import UnitTestInit
from unit_test.product.sql.sql_post import *
from unit_test.product.product_model import get_product_model
from unit_test.product.test_product_utilities import *

import time


class ProductRoutePost(unittest.TestCase):

    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    public_url = unit_test_init.create_tunnel()
    sql = PostSql(engine=engine, session=session)

    def tearDown(self):
        self.sql.delete_all_product()

    def test_create_product(self):
        print(">>> test_create_product")
        new_product = get_product_model()
        resp = requests.post(self.public_url + '/api/products'.format(), json=new_product)
        self.assertEqual(201, resp.status_code)

    def test_product_bad(self):
        print(">>> test_product_bad")
        # try to create product with error
        product_model = get_product_model()
        for key in product_model:
            print("Try with removing : {}".format(key))
            new_product = product_model.copy()
            new_product.pop(key, None)
            resp = requests.post(self.public_url + '/api/products'.format(), json=new_product)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403 \n\n#####" + resp.text)
            time.sleep(0.5)

    def test_expiration_wrong_info(self):
        print(">>> test_expiration_date_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('expiration_date')
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            new_product = get_product_model({'expiration_date': fuzzing_data[key]})
            resp = requests.post(self.public_url + '/api/products'.format(), json=new_product)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403 \n\n#####" + resp.text)
            time.sleep(0.5)

    def test_id_rfid_wrong_info(self):
        print(">>> test_id_rfid_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('id_rfid')
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            new_product = get_product_model({'id_rfid': fuzzing_data[key]})
            resp = requests.post(self.public_url + '/api/products'.format(), json=new_product)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403 \n\n#####" + resp.text)
            time.sleep(0.5)

    def test_id_ean_wrong_info(self):
        print(">>> test_id_ean_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('id_ean')
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            new_product = get_product_model({'id_ean': fuzzing_data[key]})
            resp = requests.post(self.public_url + '/api/products'.format(), json=new_product)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403 \n\n#####" + resp.text)
            time.sleep(0.5)

    def test_position_wrong_info(self):
        print(">>> test_position_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('position')
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            new_product = get_product_model({'position': fuzzing_data[key]})
            resp = requests.post(self.public_url + '/api/products'.format(), json=new_product)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403 \n\n#####" + resp.text)
            time.sleep(0.5)


if __name__ == '__main__':
    unittest.main()
