from urllib.parse import urlencode

import arrow
from flask import make_response, render_template, redirect, request

from API.Utilities import HttpRequestValidator
from API.Utilities.HttpResponse import HttpResponse, ErrorCode
from API.auth.OAuthRequestAbstract import OAuthRequestAbstract
from bdd.db_connection import session, User, AccessToken


class PostAuthorization(OAuthRequestAbstract):
    def __check_values(self):
        if request.form.get('client_id') != request.values.get('client_id'):
            raise Exception('Client ID was not recognized')

        if request.form.get('state') != request.values.get('state'):
            raise Exception('State was not recognized')

        if request.form.get('redirect_uri') != request.values.get('redirect_uri'):
            raise Exception('Redirect URI was not recognized')

    def __build_redirect_uri(self, code):
        base_uri = request.form.get('redirect_uri')
        print(code)
        args = {
            "code": code.token,
            "state": request.form.get('state')
        }
        params = urlencode(args)
        url = f"{base_uri}?{params}"
        return url

    def dispatch_request(self, request):
        validator = HttpRequestValidator.HttpRequestValidator()
        validator.throw_on_error(enabled=False)

        validator.add_param('response_type', location=HttpRequestValidator.Location.query)
        validator.add_param('client_id', location=HttpRequestValidator.Location.query)
        validator.add_param('redirect_uri', location=HttpRequestValidator.Location.query)
        app = self.get_app_with_client_id(client_id=request.values.get('client_id'))

        response_type = request.values.get('response_type')
        if response_type != 'code':
            raise Exception('Unsupported response_type')

        self.__check_values()

        if app.project_id != request.form['redirect_uri'].rsplit('/', 1)[-1]:
            return HttpResponse(403).error(ErrorCode.BAD_TOKEN)

        username = request.form.get('username')
        password = request.form.get('password')
        user = self.user_login(username=username, password=password)
        print("USERRRRRR", user)

        if user is None:
            # TODO sign-in user
            page = 'signin.html'
            # TODO how to redirect after signin ? In signin.html ?
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template(page,
                                                 client_id=request.values.get('client_id'),
                                                 redirect_uri=request.values.get('redirect_uri'),
                                                 state=request.values.get('state'),
                                                 response_type=request.values.get('response_type'),
                                                 scope=request.values.get('scope'),
                                                 year=arrow.now().format('YYYY')
                                                 ), 200, headers)
        else:
            scope = request.values.get('scope')
            code = self.create_authorization_code(app, user, "user")
            redirect_uri = self.__build_redirect_uri(code)
            return redirect(redirect_uri, code=302)
