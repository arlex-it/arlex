import unittest

import requests

from API.TestVocaleAssistant.business import get_test_vocale_assistant
from unit_test.init_unit_test import UnitTestInit


class getTestVocaleAssist(unittest.TestCase):
    def test_get_information(self):
        self.unit_test_init = UnitTestInit()

        engine, session = self.unit_test_init.connect_to_db()
        self.public_url = self.unit_test_init.create_tunnel()
        print(self.public_url + '/api/test_vocale_assistant'.format())
        resp = requests.get(self.public_url + '/api/test_vocale_assistant'.format())
        print(resp)
        self.assertEqual(200, resp.status_code)
