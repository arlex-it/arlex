from flask.views import View

from Tasker.helpers.PasswordHelper import PasswordHelper
from Tasker.helpers.exceptions import AuthError, InvalidApplication
from Tasker.helpers.generic import load_config, as_list
from Tasker.models.APIOAuthApplicationModel import APIOAuthApplicationModel
from Tasker.models.APIOAuthRefreshTokenModel import APIOAuthRefreshTokenModel
from Tasker.models.APIOAuthTokenModel import APIOAuthTokenModel
from Tasker.models.UserModel import UserModel

config = load_config()

class OAuthRequestAbstract(View):

    def check_redirect_uri(self, application, redirect_uri):
        """
        check if redirect_uri is authorized for this application
        :param application: APIOAUthApplicationModel application: An oauth application model
        :param str redirect_uri: The redirect URI you want to test
        :return: None
        """
        if not application.redirect_uri_allowed(redirect_uri=redirect_uri):
            raise AuthError('Invalid redirect uri')

    def get_app_with_client_id(self, client_id):
        """
        Try to fetch an application with the client_id


        :param client_id str: The app client_id
        :rtype: APIOAuthApplicationModel
        """

        app = APIOAuthApplicationModel.objects(appId=client_id).first()

        if not app:
            raise InvalidApplication('Invalid application : app_id.')

        if not app.is_enabled():
            raise InvalidApplication('Application is not enabled')

        return app

    def check_scope(self, application, requested_scope):
        """
        Check if the scope is authorized for this application

        :param application APIOAuathApplicationModel: An oauth applcation model
        :param requested_scope list: The scope you want to test
        :return: None
        """
        requested_scope = as_list(requested_scope)
        print(requested_scope)
        for scope in requested_scope:
            if not application.can_use_scope(scope):
                raise AuthError(f'This scope ({scope} is not available for account')

    def user_login(self, username, password):
        """
        Login an user and return it.

        :param str username: User username
        :param str password: User password
        :rtype: UserModel or None
        """
        user = UserModel.objects(emails__address=username).first()

        if user and user.is_enabled() and user.get('services.password.bcrypt'):
            current_pw = user.get('services.password.bcrypt')

            if PasswordHelper.check_password(password, current_pw):
                return user

        return None

    def create_authorization_code(self, application, entity, scope=[]):
        """
        Generate an authorization code for this application, entity, scope

        :param APIOAuthApplicationModel application: An oauth application model
        :param dict entity: Entity attached to this token
        :param list scope: List of requested scopes
        :rtype: APIOAuthTokenModel
        """
        code = APIOAuthTokenModel().create(
            app_id=application.id,
            type_='authorization_code',
            entity=entity,
            scope=scope
        )
        code.save()
        return code

    def create_access_token(self, application, entity={}, scope=[]):
        """
        Create an access token for an application, entity, and scope

        :param APIOAuthApplicationModel application: An oauth application model
        :param dict entity: Entity attached to this token
        :param list scope: List of requested scopes
        :rtype: APIOAuthTokenModel
        """
        token = APIOAuthTokenModel().create(
            app_id=application.id,
            entity=entity,
            scope=scope
        )
        token.save()
        return token

    def get_app_with_client_id_client_secret(self, client_id, client_secret):
        """
        Try to fetch an application with this client_id and client_secret

        :param str client_id: The app client_id
        :param str client_secret: The app client_secret
        :rtype: APIOAuthApplicationModel
        """
        app = APIOAuthApplicationModel.objects(appId=client_id, appSecret=client_secret).first()

        if not app:
            raise InvalidApplication('Invalid application : app_id, app_secret.')

        print(app.is_enabled())
        if not app.is_enabled():
            raise InvalidApplication('Application is not enabled')

        return app

    def check_grant_type(self, application, grant_type):
        """
        Check if this grant_type is authorized for this application

        :param APIOAuthApplicationModel application: An oauth application model
        :param str grant_type: The grant_type you want to test
        :return: None
        """
        existing_grant_type = []
        if config.get('oauth', None) and config['oauth'].get('grant_type', None):
            existing_grant_type = config['oauth']['grant_type']

        try:
            existing_grant_type.index(grant_type)
        except ValueError:
            raise AuthError('Invalid grant type')

        if not application.can_use_grant_type(grant_type):
            raise AuthError(
                f'This grant type ({grant_type}) is not available for your account'
            )

    def create_refresh_token(self, application, oauth_token):
        """
        Create a refresh token from an oauth_token

        :param APIOAuthApplicationModel application: An oauth application model
        :param APIOAuthTokenModel oauth_token: Token from which we want to generate the token
        :rtype: APIOAuthTokenModel
        """
        refresh_token = APIOAuthRefreshTokenModel().create()
        refresh_token.appId = application.id
        refresh_token.type = "refresh"
        refresh_token.oauth_token_id = oauth_token.id
        refresh_token.save()
        return refresh_token
