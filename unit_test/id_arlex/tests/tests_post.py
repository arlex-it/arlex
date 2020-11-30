import unittest

from unit_test.id_arlex.id_arlex_model import get_id_arlex_model
from unit_test.init_unit_test import UnitTestInit
from unit_test.id_arlex.sql.sql_post import *
from unit_test.Utility.sql.oauth import UtilityOauthSQL
import requests
import socket
import json


class IdArlexRoutePost(unittest.TestCase):
    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    sql = PostSql(engine=engine, session=session)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    public_url = "http://localhost:5000"
    s.close()

    def tearDown(self):
        self.sql.delete_all_id_arlex()

    def test_post_id_arlex(self):
        print('>>> test_post_id_arlex')
        new_id_arlex = get_id_arlex_model()
        resp = requests.post(self.public_url + '/api/id_arlex', json=new_id_arlex)
        self.assertEqual(201, resp.status_code)

    def test_post_already_exists_id_arlex(self):
        print('>>> test_post_already_exists_id_arlex')
        new_id_arlex = get_id_arlex_model({'patch_id': 'unique'})
        requests.post(self.public_url + '/api/id_arlex', json=new_id_arlex)
        resp = requests.post(self.public_url + '/api/id_arlex', json=new_id_arlex)
        self.assertEqual(403, resp.status_code)

    def test_post_bad_data_id_arlex(self):
        print('>>> test_post_bad_data_id_arlex')
        new_id_arlex = get_id_arlex_model()
        del new_id_arlex['patch_id']
        resp = requests.post(self.public_url + '/api/id_arlex', json=new_id_arlex)
        self.assertEqual(400, resp.status_code)


if __name__ == '__main__':
    unittest.main()
