import unittest
import requests
from unit_test.init_unit_test import UnitTestInit
from unit_test.user.sql.sql_post import *
from unit_test.user.user_model import get_user_model
from unit_test.user.test_user_utilities import *
import socket


class UserRoutePost(unittest.TestCase):
    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    sql = PostSql(engine=engine, session=session)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    public_url = "http://" + "localhost" + ":5000"
    s.close()

    def tearDown(self):
        self.sql.delete_all_user()

    def test_create_user(self):
        print(">>> test_create_user")
        new_user = get_user_model()
        resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
        self.assertEqual(201, resp.status_code)

    def test_user_already_exist(self):
        print(">>> test_user_already_exist")
        # try to create user with existing email
        new_user = get_user_model()
        self.sql.create_user(user=new_user)
        resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
        self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_gender_wrong_info(self):
        print(">>> test_gender_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('gender')
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            new_user = get_user_model({'gender': fuzzing_data[key]})
            resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_lastname_wrong_info(self):
        print(">>> test_lastname_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('lastname')
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            new_user = get_user_model({'lastname': fuzzing_data[key]})
            resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_firstname_wrong_info(self):
        print(">>> test_firstname_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('firstname')
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            new_user = get_user_model({'firstname': fuzzing_data[key]})
            resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_mail_wrong_info(self):
        print(">>> test_mail_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('mail')
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            new_user = get_user_model({'mail': fuzzing_data[key]})
            resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_password_wrong_info(self):
        print(">>> test_password_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('password')
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            new_user = get_user_model({'password': fuzzing_data[key]})
            resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_country_wrong_info(self):
        print(">>> test_country_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('country')
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            new_user = get_user_model({'country': fuzzing_data[key]})
            resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_town_wrong_info(self):
        print(">>> test_town_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('town')
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            new_user = get_user_model({'town': fuzzing_data[key]})
            resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_street_wrong_info(self):
        print(">>> test_street_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('street')
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            new_user = get_user_model({'street': fuzzing_data[key]})
            resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_street_number_wrong_info(self):
        print(">>> test_street_number_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('street_number')
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            new_user = get_user_model({'street_number': fuzzing_data[key]})
            resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_region_wrong_info(self):
        print(">>> test_region_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('region')
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            new_user = get_user_model({'region': fuzzing_data[key]})
            resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_postal_code_wrong_info(self):
        print(">>> test_postal_code_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('postal_code')
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            new_user = get_user_model({'postal_code': fuzzing_data[key]})
            resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")


if __name__ == '__main__':
    unittest.main()
