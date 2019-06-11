from flask import jsonify, request
from urllib.parse import urlencode

from Tasker.API.core import HTTPRequestValidator
from Tasker.API.core.authentication.OAuthRequestAbstract import OAuthRequestAbstract
from Tasker.helpers.exceptions import AuthError


class APICoreAuthentificationPostAuthorize(OAuthRequestAbstract):

    def __check_values(self):
        print(request.form.get('client_id'))
        print(request.values.get('client_id'))
        if request.form.get('client_id') != request.values.get('client_id'):
            raise AuthError('Client ID was not recognized')

        if request.form.get('state') != request.values.get('state'):
            raise AuthError('State was not recognized')

        if request.form.get('redirect_uri') != request.values.get('redirect_uri'):
            raise AuthError('Redirect URI was not recognized')

    def __build_redirect_uri(self, code):
        base_uri = request.form.get('redirect_uri')
        args = {
            "code:": code.token,
            "state": request.form.get('state')
        }
        params = urlencode(args)
        url = f"{base_uri}?{params}"
        return url

    def dispatch_request(self):
        #print(request.form.get('csrf_token'))
        #csrf.validate_csrf(request.form.get('csrf_token'))

        validator = HTTPRequestValidator.HTTPRequestValidator()
        validator.add_param('response_type', location=HTTPRequestValidator.Location.query)
        validator.add_param('client_id', location=HTTPRequestValidator.Location.query)
        validator.add_param('redirect_uri', location=HTTPRequestValidator.Location.query)

        response_type = request.values.get('response_type')

        if response_type != 'code':
            raise AuthError('Unsupported response_type')

        self.__check_values()

        app = self.get_app_with_client_id(client_id=request.values.get('client_id'))
        if not app.redirect_uri_allowed(redirect_uri=request.values.get('redirect_uri')):
            raise AuthError('Invalid redirect uri')

        scopes = []
        scope = request.values.get('scope')
        if scope:
            scopes = scope.split(',')
            self.check_scope(application=app, requested_scope=scopes)
        username = request.form.get('username')
        password = request.form.get('password')
        user = self.user_login(username=username, password=password)
        if user is None:
            return jsonify({'redirect': ''})

        code = self.create_authorization_code(
            application=app,
            entity={
                'type': 'user',
                'id': user.id
            },
            scope=scopes
        )
        redirect_uri = self.__build_redirect_uri(code)

        return jsonify({'redirect': redirect_uri})