import unittest
from unit_test.unit_test_template.route_name_model import get_model
from unit_test.init_unit_test import UnitTestInit
from unit_test.unit_test_template.sql.sql_request_method import *
import requests
import socket

"""
/!\ DO NOT forget to rename functions and variables /!\ 
"""


class RouteNameRouteRequestMethod(unittest.TestCase):
    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    sql = PostSql(engine=engine, session=session)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    public_url = "http://" + "localhost" + ":5000"
    s.close()

    def tearDown(self):
        self.sql.delete_all()

    # /!\ This is an example /!\
    def test_request_method_route_name(self):
        print(">>> test_[request_method]_[route_name]")
        # explain what you do in the test
        new_model = get_model()
        model_id = self.sql.create(model=new_model)
        resp = requests.delete(self.public_url + '/api/route_name/{}'.format(model_id))
        self.assertEqual(resp.status_code, 202)
        model = self.sql.get_model_by_id(model_id)
        self.assertEqual(model, None)


if __name__ == '__main__':
    unittest.main()
