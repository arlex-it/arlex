import datetime
import uuid

from flask.views import View

from API.Utilities.HttpResponse import HttpResponse, ErrorCode
from bdd.db_connection import session, Token

class OAuthRequestAbstract(View):
    def create_authorization_code(self, application, token=None):
        """
        Generate an authorization code for this application, entity, scope

        :param APIOAuthApplicationModel application: An oauth application model
        :param dict entity: Entity attached to this token
        :param list scope: List of requested scopes
        :rtype: APIOAuthTokenModel
        """
        print("coucou")
        code = Token(
            app_id=application,
            type='authorization_code',
            access_token="testt",
            date_insert= datetime.datetime.now(),
            id_user=1,
            refresh_token="test",
            expiration_date= datetime.datetime.now() + datetime.timedelta(weeks=2)
        )
        try:
            print(code)
            print("ahh")
            session.add(code)
            session.commit()
        except Exception as e:
            session.rollback()
            session.flush()
            return HttpResponse(500).error(ErrorCode.DB_ERROR, e)
        return code