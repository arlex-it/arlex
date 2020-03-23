import unittest

from flask import url_for

from bdd.db_connection import to_dict
from unit_test.user.user_model import get_user_model
from unit_test.init_unit_test import UnitTestInit
from unit_test.user.sql.sql_post import *
import requests


class OauthRouteDelete(unittest.TestCase):

    # unit_test_init = UnitTestInit()
    # engine, session = unit_test_init.connect_to_db()
    # public_url = unit_test_init.create_tunnel()
    # sql = PostSql(engine=engine, session=session)
    unit_test_init = UnitTestInit()
    engine, session = unit_test_init.connect_to_db()
    # print("url de ngrok = ", unit_test_init.create_tunnel())
    sql = PostSql(engine=engine, session=session)
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print("==========  ", s.getsockname()[0])
    public_url = "http://" + "localhost" + ":5000"
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
        token = {
            "client_id": "12151855473-vq1t07i4mg3m05jq7av9j6fh53e3eoc1.apps.googleusercontent.com",
            "client_secret": "test",
            "grant_type": "password",
            "app_id": "arlex-ccevqe",
            "username": "john@doe.com",
            "password": "password"
        }
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

            token = {"client_id"    : "12151855473-vq1t07i4mg3m05jq7av9j6fh53e3eoc1.apps.googleusercontent.com",
                     "client_secret": "test", "grant_type": "password", "app_id": "arlex-ccevqe",
                     "username"     : "john@doe.com", "password": "password", invalid: "bad"}
            resp = requests.post(self.public_url + '/api/token'.format(), json=token)
            find = resp.content.decode().title().casefold().find("<Title>Exception: Invalid Username Or Password".casefold())
            self.assertNotEqual(-1, find)

        print("         >> test_invalid_client_id")
        token = {"client_id"    : "bad",
                 "client_secret": "test", "grant_type": "password", "app_id": "arlex-ccevqe",
                 "username"     : "john@doe.com", "password": "password"}
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

        token = {
            "client_id": "12151855473-vq1t07i4mg3m05jq7av9j6fh53e3eoc1.apps.googleusercontent.com",
            "client_secret": "test",
            "grant_type": "refresh_token",
            "app_id": "arlex-ccevqe",
            "username": "john@doe.com",
            "password": "password",
            "refresh_token": refresh_token
        }
        resp = requests.post(self.public_url + '/api/token'.format(), json=token)
        self.assertEqual(200, resp.status_code)

    def test_get_invalid_refresh_token(self):
        print(">>> test_get_invalid_refresh_token")

        new_user = get_user_model()
        resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
        print("         >> create_user")
        self.assertEqual(201, resp.status_code)

        print("         >> test_invalid_refresh_token")

        token = {"client_id"    : "12151855473-vq1t07i4mg3m05jq7av9j6fh53e3eoc1.apps.googleusercontent.com",
                 "client_secret": "test", "grant_type": "refresh_token", "app_id": "arlex-ccevqe",
                 "username"     : "john@doe.com", "password": "password", "refresh_token": "bad"}
        resp = requests.post(self.public_url + '/api/token'.format(), json=token)
        find = resp.content.decode().title().casefold().find("<Title>Exception: Refresh token not found.".casefold())
        self.assertNotEqual(-1, find)

        print("         >> test_invalid_client_id")
        token = {"client_id"    : "bad",
                 "client_secret": "test", "grant_type": "password", "app_id": "arlex-ccevqe",
                 "username"     : "john@doe.com", "password": "password"}
        resp = requests.post(self.public_url + '/api/token'.format(), json=token)
        find = resp.content.decode().title().casefold().find("<Title>Exception: Invalid application : app_id.".casefold())
        self.assertNotEqual(-1, find)

    def test_get_valid_authorization_code(self):
        print(">>> test_get_valid_authorization_code")

        new_user = get_user_model()
        resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
        self.assertEqual(201, resp.status_code)
        code = resp.json()['extra']['access_token']
        token = {
            "client_id": "12151855473-vq1t07i4mg3m05jq7av9j6fh53e3eoc1.apps.googleusercontent.com",
            "client_secret": "test",
            "grant_type": "authorization_code",
            "app_id": "arlex-ccevqe",
            "username": "john@doe.com",
            "password": "authorization_code",
            "code": code,
            "redirect_uri": ""
        }
        resp = requests.post(self.public_url + '/api/token'.format(), json=token)
        self.assertEqual(200, resp.status_code)

    def test_get_invalid_authorization_code(self):
        print(">>> test_get_invalid_authorization_code")

        new_user = get_user_model()
        resp = requests.post(self.public_url + '/api/user'.format(), json=new_user)
        print("         >> create_user")
        self.assertEqual(201, resp.status_code)

        print("         >> test_invalid_authorization_code")

        token = {"client_id"    : "12151855473-vq1t07i4mg3m05jq7av9j6fh53e3eoc1.apps.googleusercontent.com",
                 "client_secret": "test", "grant_type": "authorization_code", "app_id": "arlex-ccevqe",
                 "username"     : "john@doe.com", "password": "password", "code": "bad", "redirect_uri": ""}
        resp = requests.post(self.public_url + '/api/token'.format(), json=token)
        find = resp.content.decode().title().casefold().find("<Title>Exception: Missing valid code".casefold())
        self.assertNotEqual(-1, find)

        print("         >> test_invalid_client_id")
        token = {"client_id"    : "bad",
                 "client_secret": "test", "grant_type": "password", "app_id": "arlex-ccevqe",
                 "username"     : "john@doe.com", "password": "password"}
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
        self.assertEqual("""<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Connexion à Arlex</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Quicksand">
    </head>
    <body>
        <form class="form-signin" method="POST" action="{}">
              <p class="title">Connexion Arlex</p>

              <div class="form-group form-inline">
                <input id="inputUsername" name="username" type="email" class="form-control" placeholder="Adresse mail" required>
              </div>

              <div class="form-group form-inline">
                <input id="inputPassword" name="password" type="password" class="form-control" placeholder="Mot de passe" required>
              </div>

              <a class="form-text forgotten" href="#">Mot de passe oublié ?</a>
              <button id="submit_button" class="btn">Se connecter</button>

              <input type="hidden" name="state" value="{}">
              <input type="hidden" name="client_id" value="{}">
              <input type="hidden" name="redirect_uri" value="{}">
              <input type="hidden" name="response_type" value="{}"/>
              <input type="hidden" name="scope" value="{}"/>
        </form>
     <script language="JavaScript" src="/static/js/authorization.js"></script>
    </body>

</html>""".format("/api/auth/authorize", state, client_id, redirect_uri, response_type, scope), resp.content.decode())


if __name__ == '__main__':
    unittest.main()
