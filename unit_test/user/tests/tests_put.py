import unittest
import requests
from unit_test.user.user_model import get_user_model
from unit_test.init_unit_test import UnitTestInit
from unit_test.user.sql.sql_post import *
from unit_test.user.test_user_utilities import *
from unit_test.Utility.sql.oauth import UtilityOauthSQL
import socket


class MyTestCase(unittest.TestCase):
    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    sql = PostSql(engine=engine, session=session)
    oauth_sql = UtilityOauthSQL(engine=engine, session=session)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    public_url = "http://localhost:5000"
    s.close()

    def tearDown(self):
        self.sql.delete_all_user()

    def test_update_user(self):
        print(">>> test_update_user")
        new_user = get_user_model()
        user_id = self.sql.create_user(user=new_user)
        update_user = {
            "gender": 1,
            "lastname": "Does",
            "firstname": "Jane",
            "mail": "jane@does.com",
            "password": "mypassword",
            "country": "Belgique",
            "town": "Bruxelles",
            "street": "rue test",
            "street_number": "45",
            "region": "une region",
            "postal_code": "54321"
        }
        # create user token
        token = self.oauth_sql.create_default_access_token(id_user=user_id)
        resp = requests.put(self.public_url + '/api/user/{}'.format(user_id), json=update_user, headers={'Authorization': 'Bearer ' + token['token']})
        self.assertEqual(202, resp.status_code)

    def test_update_mail_already_exist(self):
        print(">>> test_update_mail_already_exist")
        new_user = get_user_model()
        other_user = get_user_model({
            "gender": 1,
            "lastname": "Does",
            "firstname": "Jane",
            "mail": "jane@does.com",
            "password": "mypassword",
            "country": "Belgique",
            "town": "Bruxelles",
            "street": "rue test",
            "street_number": "45",
            "region": "une region",
            "postal_code": "54321"
        })
        user_id = self.sql.create_user(user=new_user)
        self.sql.create_user(user=other_user)
        update_user = {"mail": "jane@does.com"}
        # create user token
        token = self.oauth_sql.create_default_access_token(id_user=user_id)
        resp = requests.put(self.public_url + '/api/user/{}'.format(user_id), json=update_user, headers={'Authorization': 'Bearer ' + token['token']})
        self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_update_password_wrong_info(self):
        print(">>> test_update_password_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('password')
        new_user = get_user_model()
        user_id = self.sql.create_user(user=new_user)
        # create user token
        token = self.oauth_sql.create_default_access_token(id_user=user_id)
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            update_user = {'password': fuzzing_data[key]}
            resp = requests.put(self.public_url + '/api/user/{}'.format(user_id), json=update_user, headers={'Authorization': 'Bearer ' + token['token']})
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_update_lastname_wrong_info(self):
        print(">>> test_update_lastname_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('lastname')
        new_user = get_user_model()
        user_id = self.sql.create_user(user=new_user)
        # create user token
        token = self.oauth_sql.create_default_access_token(id_user=user_id)
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            update_user = {'lastname': fuzzing_data[key]}
            resp = requests.put(self.public_url + '/api/user/{}'.format(user_id), json=update_user, headers={'Authorization': 'Bearer ' + token['token']})
            print(resp.text)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_udapte_firstname_wrong_info(self):
        print(">>> test_udapte_firstname_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('firstname')
        new_user = get_user_model()
        user_id = self.sql.create_user(user=new_user)
        # create user token
        token = self.oauth_sql.create_default_access_token(id_user=user_id)
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            update_user = {'firstname': fuzzing_data[key]}
            resp = requests.put(self.public_url + '/api/user/{}'.format(user_id), json=update_user, headers={'Authorization': 'Bearer ' + token['token']})
            print(resp.text)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_update_mail_wrong_info(self):
        print(">>> test_update_mail_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('mail')
        new_user = get_user_model()
        user_id = self.sql.create_user(user=new_user)
        # create user token
        token = self.oauth_sql.create_default_access_token(id_user=user_id)
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            update_user = {'mail': fuzzing_data[key]}
            resp = requests.put(self.public_url + '/api/user/{}'.format(user_id), json=update_user, headers={'Authorization': 'Bearer ' + token['token']})
            print(resp.text)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_update_gender_wrong_info(self):
        print(">>> test_update_gender_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('gender')
        new_user = get_user_model()
        user_id = self.sql.create_user(user=new_user)
        # create user token
        token = self.oauth_sql.create_default_access_token(id_user=user_id)
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            update_user = {'gender': fuzzing_data[key]}
            resp = requests.put(self.public_url + '/api/user/{}'.format(user_id), json=update_user, headers={'Authorization': 'Bearer ' + token['token']})
            print(resp.text)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_update_country_wrong_info(self):
        print(">>> test_update_country_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('country')
        new_user = get_user_model()
        user_id = self.sql.create_user(user=new_user)
        # create user token
        token = self.oauth_sql.create_default_access_token(id_user=user_id)
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            update_user = {'country': fuzzing_data[key]}
            resp = requests.put(self.public_url + '/api/user/{}'.format(user_id), json=update_user, headers={'Authorization': 'Bearer ' + token['token']})
            print(resp.text)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_update_town_wrong_info(self):
        print(">>> test_update_town_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('town')
        new_user = get_user_model()
        user_id = self.sql.create_user(user=new_user)
        # create user token
        token = self.oauth_sql.create_default_access_token(id_user=user_id)
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            update_user = {'town': fuzzing_data[key]}
            resp = requests.put(self.public_url + '/api/user/{}'.format(user_id), json=update_user, headers={'Authorization': 'Bearer ' + token['token']})
            print(resp.text)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_update_street_wrong_info(self):
        print(">>> test_update_street_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('street')
        new_user = get_user_model()
        user_id = self.sql.create_user(user=new_user)
        # create user token
        token = self.oauth_sql.create_default_access_token(id_user=user_id)
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            update_user = {'street': fuzzing_data[key]}
            resp = requests.put(self.public_url + '/api/user/{}'.format(user_id), json=update_user, headers={'Authorization': 'Bearer ' + token['token']})
            print(resp.text)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_update_street_number_wrong_info(self):
        print(">>> test_update_street_number_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('street_number')
        new_user = get_user_model()
        user_id = self.sql.create_user(user=new_user)
        # create user token
        token = self.oauth_sql.create_default_access_token(id_user=user_id)
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            update_user = {'street_number': fuzzing_data[key]}
            resp = requests.put(self.public_url + '/api/user/{}'.format(user_id), json=update_user, headers={'Authorization': 'Bearer ' + token['token']})
            print(resp.text)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_update_region_wrong_info(self):
        print(">>> test_update_region_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('region')
        new_user = get_user_model()
        user_id = self.sql.create_user(user=new_user)
        # create user token
        token = self.oauth_sql.create_default_access_token(id_user=user_id)
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            update_user = {'region': fuzzing_data[key]}
            resp = requests.put(self.public_url + '/api/user/{}'.format(user_id), json=update_user, headers={'Authorization': 'Bearer ' + token['token']})
            print(resp.text)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")

    def test_update_postal_code_wrong_info(self):
        print(">>> test_update_postal_code_wrong_info")
        fuzzing_data = get_fuzzing_data_by_input('postal_code')
        new_user = get_user_model()
        user_id = self.sql.create_user(user=new_user)
        # create user token
        token = self.oauth_sql.create_default_access_token(id_user=user_id)
        for key in fuzzing_data:
            print_arg(fuzzing_data[key])
            update_user = {'postal_code': fuzzing_data[key]}
            resp = requests.put(self.public_url + '/api/user/{}'.format(user_id), json=update_user, headers={'Authorization': 'Bearer ' + token['token']})
            print(resp.text)
            self.assertTrue(resp.status_code == 400 or resp.status_code == 403, str(resp.status_code) + " != 400 | 403")
            

if __name__ == '__main__':
    unittest.main()
