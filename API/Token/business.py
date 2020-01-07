import datetime

import arrow
from flask import jsonify
from flask_restplus import abort

from API.Utilities.HttpRequest import HttpRequest
from API.Utilities.HttpRequestValidator import HttpRequestValidator
from API.Utilities.HttpResponse import HttpResponse, SuccessCode
from bdd.db_connection import Token, session


class PostToken():
    def __grant_authorization_code(self):
        validator = HttpRequestValidator()
        validator.throw_on_error(False)
        validator.add_param('code', True)
        validator.add_param('redirect_uri', True)
        if not validator.verify():
            raise Exception('Invalid code')

        print(self.__request.get_param('redirect_uri'))

        print(self.__request.get_param('code'))
        code = session.query(Token).filter(Token.access_token == self.__request.get_param('code')).first()
        print(code)
        token = Token(
            app_id=self.app_id,
            type='authorization_code',
            access_token="access_token",
            date_insert=datetime.datetime.now(),
            id_user=1,
            refresh_token="test2",
            expiration_date=datetime.datetime.now() + datetime.timedelta(weeks=2)
                      )
        refresh_token = Token(
            app_id=self.app_id,
            type='authorization_code',
            access_token="no",
            date_insert=datetime.datetime.now(),
            id_user=1,
            refresh_token="Refresh",
            expiration_date=datetime.datetime.now() + datetime.timedelta(weeks=2)

        )

        print("yo")
        return token, refresh_token

    def dispatch_request(self, request):
        self.__request = HttpRequest()
        self.application_id = self.__request.get_param('client_id')
        self.application_secret = self.__request.get_param('client_secret')
        self.grant_type = self.__request.get_param('grant_type')
        self.app_id = self.__request.get_param('app_id')
        print(self.application_id)
        print(self.application_secret)
        print(request)
        print(self.app_id)
        print(self.grant_type)
        token = None
        refresh_token = None
        if self.grant_type == 'authorization_code':
            token, refresh_token = self.__grant_authorization_code()
        return HttpResponse(200).custom({"token_type": token.type,
                                         "access_token": token.refresh_token,
                                         "expire_at": token.expiration_date.isoformat(),
                                         'expires_in': round(arrow.get(token.expiration_date).float_timestamp - arrow.now().float_timestamp),
                                         'refresh_token': refresh_token.refresh_token
                                        })