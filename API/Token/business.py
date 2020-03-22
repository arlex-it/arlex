import datetime
import uuid

import arrow

from API.Utilities.HttpRequest import HttpRequest
from API.Utilities.PasswordUtilities import PasswordUtilities
from API.Utilities.HttpRequestValidator import HttpRequestValidator
from API.Utilities.HttpResponse import HttpResponse, ErrorCode
from bdd.db_connection import AccessToken, session, User, RefreshToken
from API.auth.OAuthRequestAbstract import OAuthRequestAbstract


class PostToken(OAuthRequestAbstract):
    def __init__(self):
        self.__request = HttpRequest()
        self.application_id = self.get_app_with_client_id(client_id=self.__request.get_param('client_id')).id
        self.application_secret = self.__request.get_param('client_secret')
        self.grant_type = self.__request.get_param('grant_type')
        self.app_id = self.__request.get_param('app_id')

    def get_user(self, user_id):
        """
        :rtype: UserModel, ProModel or None
        """
        user = session.query(User).filter(User.id == user_id).first()
        return user

    def get_response_dict(self, token, refresh_token):
        """
        :param APIOAuthTokenModel token:
        :rtype: dict
        """

        resp = {
            "token_type": token.type,
            "access_token": token.token,
            "expire_at": token.expiration_date.isoformat(),
            'expires_in': round(arrow.get(token.expiration_date).float_timestamp - arrow.now().float_timestamp),
        }

        if refresh_token:
            resp['refresh_token'] = refresh_token.token

        return resp

    def grant_authorization_code(self):
        validator = HttpRequestValidator()
        validator.throw_on_error(False)
        validator.add_param('code', True)
        validator.add_param('redirect_uri', True)
        if not validator.verify():
            raise Exception('Invalid code')

        code = session.query(AccessToken).filter(AccessToken.token == self.__request.get_param('code')).first()
        if code is None or code.is_enable == 0:
            raise Exception('Missing valid code')
        info = {
            "is_enable": 0
        }

        try:
            session.begin()
            session.query(AccessToken).filter(AccessToken.id == code.id).update(info)
            session.commit()
        except Exception as e:
            session.rollback()
            session.flush()
            return HttpResponse(500).error(ErrorCode.DB_ERROR, e)

        if str(code.app_id) != str(self.application_id):
            raise Exception('Code does not match your app_id.')
        user = self.get_user(code.id_user)
        if not user or user.is_active == 0:
            raise Exception('Cannot authorize. Account is disabled.')

        access_token = AccessToken(
            app_id=self.application_id,
            type='Bearer',
            token=uuid.uuid4().hex[:35],
            date_insert=datetime.datetime.now(),
            id_user=user.id,
            expiration_date=arrow.now().shift(hours=+10).datetime,
            is_enable=1
        )
        try:
            session.begin()
            session.add(access_token)
            session.commit()
        except Exception as e:
            session.rollback()
            session.flush()
            return HttpResponse(500).error(ErrorCode.DB_ERROR, e)

        refresh_token = RefreshToken(
            app_id=self.application_id,
            date_insert=datetime.datetime.now(),
            token=uuid.uuid4().hex[:35],
            is_enable=True,
            access_token_id=access_token.id,
        )
        try:
            session.begin()
            session.add(refresh_token)
            session.commit()
        except Exception as e:
            session.rollback()
            session.flush()
            return HttpResponse(500).error(ErrorCode.DB_ERROR, e)
        return access_token, refresh_token

    def grant_password(self):
        print("eheh")
        validator = HttpRequestValidator()
        validator.throw_on_error(True)
        validator.add_param('username', True)
        validator.add_param('password', True)

        if validator.verify():

            username = self.__request.get_param('username')
            print(username)
            username = username.lower()
            user = session.query(User).filter(User.mail == username).first()
            if user and user.is_active != 0 and user.password:
                current_pw = user.password

                password = self.__request.get_param('password')
                print(password)

                if PasswordUtilities.check_password(password, current_pw):
                    scope = "user"
                    access_token = AccessToken(
                        app_id=self.application_id,
                        type='bearer',
                        token=uuid.uuid4().hex[:35],
                        date_insert=datetime.datetime.now(),
                        id_user=user.id,
                        expiration_date=arrow.now().shift(hours=+10).datetime,
                        is_enable=1,
                        scopes='user'
                    )
                    try:
                        session.begin()
                        session.add(access_token)
                        session.commit()
                    except Exception as e:
                        session.rollback()
                        session.flush()
                        return HttpResponse(500).error(ErrorCode.DB_ERROR, e)

                    refresh_token = RefreshToken(
                        app_id=self.application_id,
                        date_insert=datetime.datetime.now(),
                        token=uuid.uuid4().hex[:35],
                        is_enable=True,
                        access_token_id=access_token.id,
                    )
                    try:
                        session.begin()
                        session.add(refresh_token)
                        session.commit()
                    except Exception as e:
                        session.rollback()
                        session.flush()
                        return HttpResponse(500).error(ErrorCode.DB_ERROR, e)
                    return access_token, refresh_token
                else:
                    raise Exception('Invalid username or password')
            else:
                raise Exception('Invalid username or password')

    def grant_refresh_token(self):
        validator = HttpRequestValidator()
        validator.throw_on_error(True)
        validator.add_param('refresh_token', True)

        if validator.verify():
            refresh_token = session.query(RefreshToken).filter(RefreshToken.token == self.__request.get_param('refresh_token')).first()
            if not refresh_token:
                raise Exception('Refresh token not found.')
            
            if not refresh_token.is_enable:
                raise Exception('Refresh token is invalid.')
            
            if str(refresh_token.app_id) != str(self.application_id):
                raise Exception('Code does not match your app_id.')

            old_token = session.query(AccessToken).filter(
                AccessToken.token == RefreshToken.access_token_id).first()
            info = {
                "is_enable": 0
            }
            try:
                session.begin()
                session.query(AccessToken).filter(AccessToken.id == old_token.id).update(info)
                session.commit()
            except Exception as e:
                session.rollback()
                session.flush()
                return HttpResponse(500).error(ErrorCode.DB_ERROR, e)
            user = self.get_user(old_token.id_user)
            if not user or user.is_active == 0:
                raise Exception('Cannot authorize. Account is disabled.')
            access_token = AccessToken(
                app_id=self.application_id,
                type='bearer',
                token=uuid.uuid4().hex[:35],
                date_insert=datetime.datetime.now(),
                id_user=user.id,
                expiration_date=arrow.now().shift(hours=+10).datetime,
                is_enable=1
            )
            try:
                session.begin()
                session.add(access_token)
                session.commit()
            except Exception as e:
                session.rollback()
                session.flush()
                return HttpResponse(500).error(ErrorCode.DB_ERROR, e)

            refresh_token = RefreshToken(
                app_id=self.application_id,
                date_insert=datetime.datetime.now(),
                token=uuid.uuid4().hex[:35],
                is_enable=True,
                access_token_id=access_token.id,
            )
            try:
                session.begin()
                session.add(refresh_token)
                session.commit()
            except Exception as e:
                session.rollback()
                session.flush()
                return HttpResponse(500).error(ErrorCode.DB_ERROR, e)

            return access_token, refresh_token

    def dispatch_request(self, request):
        token = None
        refresh_token = None
        if self.grant_type == 'authorization_code':
            (token, refresh_token) = self.grant_authorization_code()
        elif self.grant_type == 'refresh_token':
            (token, refresh_token) = self.grant_refresh_token()
        elif self.grant_type == 'password':
            (token, refresh_token) = self.grant_password()
        context = self.get_response_dict(token, refresh_token)
        return HttpResponse(200).custom(context)