import unittest

import requests
from unit_test.init_unit_test import UnitTestInit
from unit_test.user.sql.sql_post import *
from unit_test.user.test_user_utilities import *
import socket


class getTestVocaleAssist(unittest.TestCase):
    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    sql = PostSql(engine=engine, session=session)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    public_url = "http://localhost:5000"
    s.close()

    def test_get_information(self):
        resp = requests.get(self.public_url + '/api/test_vocale_assistant'.format())
        self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

if __name__ == '__main__':
    unittest.main()