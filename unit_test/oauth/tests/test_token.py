import unittest

from unit_test.oauth.user_model import get_user_model
from unit_test.init_unit_test import UnitTestInit
from unit_test.oauth.sql.sql_post import *
from unit_test.oauth.test_token_utilities import get_token_template, get_form_template
import requests
import socket


class OauthRouteDelete(unittest.TestCase):
    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    sql = PostSql(engine=engine, session=session)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    public_url = "http://localhost:5000"
    s.close()

    def setUp(self):
        self.sql.delete_all_user()
        self.sql.add_application_auth()

    def tearDown(self):
        self.sql.delete_all_user()
        self.sql.add_application_auth()

    def test_get_valid_token_password(self):
        print(">>> test_get_valid_token_password")

        new_user = get_user_model()
        resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
        self.assertEqual(201, resp.status_code)
        token = get_token_template()
        resp = requests.post(self.public_url + '/api/token'.format(), json=token)
        self.assertEqual(200, resp.status_code)

    def test_get_invalid_token_password(self):
        print(">>> test_get_invalid_token_password")

        new_user = get_user_model()
        resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
        print("         >> create_user")
        self.assertEqual(201, resp.status_code)

        for invalid in ['password', 'username']:
            print("         >> test_invalid_", invalid)
            token = get_token_template()
            token[invalid] = "bad"
            resp = requests.post(self.public_url + '/api/token'.format(), json=token)
            find = resp.content.decode().title().casefold().find("<Title>Exception: Invalid Username Or Password".casefold())
            self.assertNotEqual(-1, find)

        print("         >> test_invalid_client_id")
        token = get_token_template()
        token['client_id'] = "bad"
        resp = requests.post(self.public_url + '/api/token'.format(), json=token)
        find = resp.content.decode().title().casefold().find("<Title>Exception: Invalid application : app_id.".casefold())
        self.assertNotEqual(-1, find)

    def test_valid_refresh_token(self):
        print(">>> test_valid_refresh_token")

        new_user = get_user_model()
        resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
        print("         >> create_user")
        refresh_token = resp.json()['extra']['refresh_token']
        self.assertEqual(201, resp.status_code)

        token = get_token_template()
        token['grant_type'] = "refresh_token"
        token['refresh_token'] = refresh_token
        resp = requests.post(self.public_url + '/api/token'.format(), json=token)
        self.assertEqual(200, resp.status_code)

    def test_get_invalid_refresh_token(self):
        print(">>> test_get_invalid_refresh_token")

        new_user = get_user_model()
        resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
        print("         >> create_user")
        self.assertEqual(201, resp.status_code)

        print("         >> test_invalid_refresh_token")
        token = get_token_template()
        token["grant_type"] = "refresh_token"
        token['refresh_token'] = "bad"
        resp = requests.post(self.public_url + '/api/token'.format(), json=token)
        find = resp.content.decode().title().casefold().find("<Title>Exception: Refresh token not found.".casefold())
        self.assertNotEqual(-1, find)

        print("         >> test_invalid_client_id")
        token = get_token_template()
        token['client_id'] = "bad"
        resp = requests.post(self.public_url + '/api/token'.format(), json=token)
        find = resp.content.decode().title().casefold().find("<Title>Exception: Invalid application : app_id.".casefold())
        self.assertNotEqual(-1, find)

    def test_get_valid_authorization_code(self):
        print(">>> test_get_valid_authorization_code")

        new_user = get_user_model()
        resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
        self.assertEqual(201, resp.status_code)
        code = resp.json()['extra']['access_token']

        token = get_token_template()
        token["grant_type"] = "authorization_code"
        token["password"] = "authorization_code"
        token["code"] = code
        token["redirect_uri"] = ""
        resp = requests.post(self.public_url + '/api/token'.format(), json=token)
        self.assertEqual(200, resp.status_code)

    def test_get_invalid_authorization_code(self):
        print(">>> test_get_invalid_authorization_code")

        new_user = get_user_model()
        resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
        print("         >> create_user")
        self.assertEqual(201, resp.status_code)

        print("         >> test_invalid_authorization_code")
        token = get_token_template()
        token['grant_type'] = "authorization_code"
        token['code'] = "bad"
        token['redirect_uri'] = ""
        resp = requests.post(self.public_url + '/api/token'.format(), json=token)
        find = resp.content.decode().title().casefold().find("<Title>Exception: Missing valid code".casefold())
        self.assertNotEqual(-1, find)

        print("         >> test_invalid_client_id")
        token = get_token_template()
        token['client_id'] = "bad"
        resp = requests.post(self.public_url + '/api/token'.format(), json=token)
        find = resp.content.decode().title().casefold().find("<Title>Exception: Invalid application : app_id.".casefold())
        self.assertNotEqual(-1, find)

    def test_get_authorize_route(self):
        print(">>> test_get_authorize_route")
        state = "AMXHz3TJp9asTcwX21jl2YfbTE7i3Ou0m--bj4QylQ-wRm6llYEmP12v7vH5T0Z1burSoWW6gszPTsfhDdSG_0t9RmRF0msF1w6jnKl4lLRHYerPZh_VBjm0h9aEJsUbglgGsQBSdTqUJB0RjJgXG1zXma_I3oomoSZQlo1pZWTtMsOLNLtkNU-Dqr_10m4GF7NPIu6XYj7ZReFyUpSleOeKn__vB8mnmYcCyWw1YcpGMHIZ9PHgVgF5Fm04SvAnZIxGEaMscF1mQdRZv6YTr0PZurzvdMcJVBIUshjVrQLasfCMzrMuekHFHfaSKHPQepL1tuSgws8blDXKGs4oCJxoENlKZpn7yZVc_59DnSu_8dwLbIcrW1GfqRujw87kJERa0jxJEAb99-4YK7Vxahjlfq5PYf_kfkq5-CiGs2m2a7LwP3p4Ljg7uDiB4ND1bEpKVm_2R1GYEOn540GOBsyUKZcgTIqb0M7spOXGxdVMYdLLqv9waOzHNM8kCJbMM2tWIzhGAflfJV2tVW7AGuULzKVMkTnQv6hGOc13-9w0J3taX-hZJDo"
        client_id = "12151855473-vq1t07i4mg3m05jq7av9j6fh53e3eoc1.apps.googleusercontent.com"
        response_type = "code"
        redirect_uri = "https://oauth-redirect.googleusercontent.com/r/arlex-ccevqe"
        scope = ""
        resp = requests.get(self.public_url + '/api/auth/authorize?'
                                              'client_id=' + client_id +
                                              '&state=' + state +
                                              '&response_type=' + response_type +
                                              '&redirect_uri=' + redirect_uri.format())

        find = [resp.content.decode().find("""<input type="hidden" name="state" value="{}">""".format(state)),
                resp.content.decode().find(
                    """<input type="hidden" name="client_id" value="{}">""".format(client_id)),
                resp.content.decode().find(
                    """<input type="hidden" name="redirect_uri" value="{}">""".format(redirect_uri)),
                resp.content.decode().find(
                    """<input type="hidden" name="response_type" value="{}"/>""".format(response_type)),
                resp.content.decode().find("""<input type="hidden" name="scope" value="{}"/>""".format(scope))]

        self.assertEqual(False, -1 in find)

    def test_post_authorize_route(self):
        print(">>> test_post_authorize_route")
        new_user = get_user_model()
        resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
        print("         >> create_user")
        self.assertEqual(201, resp.status_code)
        form = get_form_template(new_user)
        print("         >> connect_user_oauth")
        resp = requests.post(self.public_url + '/api/auth/authorize', data=form)
        self.assertEqual(200, resp.status_code)
        it = resp.url.find("https://oauth-redirect.googleusercontent.com/")
        self.assertNotEqual(-1, it)

    def test_invalid_post_authorize_route(self):
        print(">>> test_invalid_post_authorize_route")
        new_user = get_user_model()
        resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
        print("         >> create_user")
        self.assertEqual(201, resp.status_code)

        for bad in ['state', 'client_id', 'response_type', 'redirect_uri', 'username', 'password']:
            form = get_form_template(new_user)
            form[bad] = "bad"
            print("         >> invalid_" + bad + "_user_oauth")
            resp = requests.post(self.public_url + '/api/auth/authorize', data=form)
            if resp.status_code == 200:
                it = resp.text.find("<title>S'inscrire</title>")
                self.assertNotEqual(it, -1)
            else:
                self.assertNotEqual(200, resp.status_code)


if __name__ == '__main__':
    unittest.main()
