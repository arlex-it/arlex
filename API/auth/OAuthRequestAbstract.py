import datetime
import uuid

from flask.views import View

from API.Utilities.HttpResponse import HttpResponse, ErrorCode
from bdd.db_connection import session, AccessToken, AuthApplication, User
from API.User.business import check_password


class OAuthRequestAbstract(View):
    def create_authorization_code(self, application, user):
        """
        Generate an authorization code for this application, entity, scope

        :param APIOAuthApplicationModel application: An oauth application model
        :param dict entity: Entity attached to this token
        :rtype: APIOAuthTokenModel
        """
        code = AccessToken(
            app_id=application.id,
            type='authorization_code',
            token=uuid.uuid4().hex[:35],
            date_insert=datetime.datetime.now(),
            id_user=user.id,
            expiration_date=datetime.datetime.now() + datetime.timedelta(weeks=2),
            is_enable=1
        )
        try:
            session.begin()
            session.add(code)
            session.commit()
        except Exception as e:
            session.rollback()
            session.flush()
            return HttpResponse(500).error(ErrorCode.DB_ERROR, e)
        return code

    def get_app_with_client_id(self, client_id):
        """
        Try to fetch an application with this client_id

        :param str client_id: The app client_id
        :rtype: APIOAuthApplicationModel

        """
        app = session.query(AuthApplication).filter(AuthApplication.client_id == client_id).first()

        if not app:
            raise Exception('Invalid application : app_id.')

        return app

    def user_login(self, username, password):
        """
        Login an user and return it.

        :param str username: User username
        :param str password: User password
        :rtype: UserModel or None
        """

        user = session.query(User) \
            .join(AccessToken, User.id == AccessToken.id_user) \
            .filter(User.mail == username) \
            .add_columns(User.id, User.password, AccessToken.token) \
            .first()

        #user = session.query(User).filter(User.mail == username).first()

        if user is not None:
            if check_password(password, user.password.encode()):
                return user
            else:
                return None
        else:
            return None

