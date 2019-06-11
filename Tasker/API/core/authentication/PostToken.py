import arrow

from Tasker.API.core.HTTPReponse import HTTPResponse
from Tasker.API.core.HTTPRequest import HTTPRequest
from Tasker.API.core.HTTPRequestValidator import HTTPRequestValidator
from Tasker.API.core.authentication.OAuthRequestAbstract import OAuthRequestAbstract
from Tasker.helpers.PasswordHelper import PasswordHelper
from Tasker.helpers.exceptions import AuthError
from Tasker.models.APIOAuthTokenModel import APIOAuthTokenModel
from Tasker.models.UserModel import UserModel


class APICoreAuthenticationPostToken(OAuthRequestAbstract):
    __request = None
    __application = None

    __application_id = None
    __application_secret = None
    __grant_type = None
    __requested_scope = []
    def __get_response_dict(self, token, refresh_token):
        """
        :param APIOAuthTokenModel token:
        :rtype: dict
        """
        resp = {
            'token_type': token.type_,
            'access_token': token.token,
            'expires_at': token.expiresAt.isoformat(),
            'expires_in': round(arrow.get(token.expiresAt).float_timestamp - arrow.now().float_timestamp),
            'scopes': token.scope
        }

        if refresh_token:
            resp['refresh_token'] = refresh_token.token

        return resp

    def __grant_client_credentials(self):
        """
        :rtype: (token, None)
        """
        token = self.create_access_token(application=self.__application, scope=self.__requested_scope)
        return (token, None)

    def __grant_password(self):

        validator = HTTPRequestValidator()
        validator.throw_on_error(True)
        validator.add_param('username', True)
        validator.add_param('password', True)

        if validator.verify():

            user = UserModel.objects(emails__address=self.__request.get_param('username')).first()

            if user and user.is_enabled() and user.get('services.password.bcrypt'):
                current_pw = user.get('services.password.bcrypt')

                password = self.__request.get_param('password')

                if PasswordHelper.check_password(password, current_pw):

                    scope = [
                        'global',
                        'customer:.*',
                        'shopper:.*',
                        'mission:.*',
                        'mission_template:.*',
                        'user:.*'
                    ]

                    token = self.create_access_token(
                        application=self.__application,
                        entity={
                            'type': "user",
                            'id': user.id
                        },
                        scope=scope)

                    refresh_token = self.create_refresh_token(
                        application=self.__application,
                        oauth_token=token
                    )

                    return (token, refresh_token)
                else:
                    raise AuthError('Invalid username or password')
            else:
                raise AuthError('Invalid username or password')

    def dispatch_request(self):
        self.__request = HTTPRequest()

        self.__application = None

        self.__application_id = self.__request.get_param('app_id')
        self.__application_secret = self.__request.get_param('app_secret')

        # OAuth 2 RFC indicates that we must use client_id and client_secret and not app_id and app_secret
        if self.__request.get_param('client_id'):
            self.__application_id = self.__request.get_param('client_id')
        if self.__request.get_param('client_secret'):
            self.__application_secret = self.__request.get_param('client_secret')

        self.__grant_type = self.__request.get_param('grant_type')
        self.__requested_scope = self.__request.get_param('scope', [])

        if 'global' not in self.__requested_scope:
            self.__requested_scope.append('global')

        self.__application = self.get_app_with_client_id_client_secret(
            client_id=self.__application_id,
            client_secret=self.__application_secret
        )
        print(self)
        print(self.__grant_type)
        self.check_grant_type(self.__application, self.__grant_type)
        print("ahhh")
        self.check_scope(self.__application, self.__requested_scope)
        print("toto")
        token = None
        refresh_token = None

        if self.__grant_type == 'client_credentials':
            (token, refresh_token) = self.__grant_client_credentials()
        elif self.__grant_type == 'password':
            (token, refresh_token) = self.__grant_password()
        elif self.__grant_type == 'refresh_token':
            (token, refresh_token) = self.__grant_refresh_token()
        elif self.__grant_type == 'authorization_code':
            (token, refresh_token) = self.__grant_authorization_code()
        else:
            AuthError('Invalid grant type')

        if not token or not isinstance(token, APIOAuthTokenModel):
            raise AuthError('Authorization server refused to process this request.')

        context = self.__get_response_dict(token, refresh_token)

        return HTTPResponse(200, context).get_response()