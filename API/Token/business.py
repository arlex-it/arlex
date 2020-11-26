import datetime
import json
import uuid

import arrow
import requests

from API.User.business import create_user
from API.Utilities.HttpRequest import HttpRequest
from API.Utilities.PasswordUtilities import PasswordUtilities
from API.Utilities.HttpRequestValidator import HttpRequestValidator
from API.Utilities.HttpResponse import HttpResponse, ErrorCode, SuccessCode
from bdd.db_connection import AccessToken, session, User, RefreshToken, to_dict
from API.auth.OAuthRequestAbstract import OAuthRequestAbstract


class PostToken(OAuthRequestAbstract):
    def __init__(self):
        self.__request = HttpRequest()
        self.application_id = self.get_app_with_client_id(client_id=self.__request.get_param('client_id')).id
        self.application_secret = self.__request.get_param('client_secret')
        self.grant_type = self.__request.get_param('grant_type')
        self.app_id = self.__request.get_param('app_id')
        # self.intent = self.__request.get_param('intent')
        # self.jwt_token = self.__request.get_param('assertion')

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
        """
        make last authorization_code invalid and create a new one
        """
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
            type='bearer',
            token=uuid.uuid4().hex[:35],
            date_insert=datetime.datetime.now(),
            id_user=user.id,
            expiration_date=arrow.now().shift(hours=+10).datetime,
            is_enable=1,
            scopes="user"
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
        """
        Create access and refresh token
        """
        validator = HttpRequestValidator()
        validator.throw_on_error(True)
        validator.add_param('username', True)
        validator.add_param('password', True)

        if validator.verify():

            # verify combo username password
            username = self.__request.get_param('username')
            username = username.lower()
            user = session.query(User).filter(User.mail == username).first()
            if user and user.is_active != 0 and user.password:
                current_pw = user.password

                password = self.__request.get_param('password')

                if PasswordUtilities.check_password(password, current_pw):
                    # create new access and refresh token
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
            # check refresh token validity
            refresh_token = session.query(RefreshToken).filter(RefreshToken.token == self.__request.get_param('refresh_token')).first()
            if not refresh_token:
                raise Exception('Refresh token not found.')
            
            if not refresh_token.is_enable:
                raise Exception('Refresh token is invalid.')
            
            if str(refresh_token.app_id) != str(self.application_id):
                raise Exception('Code does not match your app_id.')

            # invalidate old refresh token and create new access and refresh token
            old_token = session.query(AccessToken).filter(
                AccessToken.id == refresh_token.access_token_id).first()
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
                is_enable=1,
                scopes="user"
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
        if self.intent == 'get':
            return HttpResponse(401).error(ErrorCode.USER_NOT_FOUND)
        if self.intent == "create":
            import jwt
            from jwt.algorithms import RSAAlgorithm
        
            # get google keys for jwt
            keys = requests.get('https://www.googleapis.com/oauth2/v3/certs').json()
            # get kid to know which key to use
            jwt_header = jwt.get_unverified_header(self.jwt_token)
            if keys['keys'][0]['kid'] == jwt_header['kid']:
                key_json = json.dumps(keys['keys'][0])
            else:
                key_json = json.dumps(keys['keys'][1])
            # get public key and then decode jwt data to get user informations
            public_key = RSAAlgorithm.from_jwk(key_json)
            user_data = jwt.decode(self.jwt_token, public_key, audience='12151855473-09qt5cef2ge0fmkj29vrqo44oqqkarvh.apps.googleusercontent.com', algorithms='RS256')
            # check user information validity
            if user_data['iss'] != 'https://accounts.google.com':
                return HttpResponse(500).error(ErrorCode.UNK)
            elif not user_data['email_verified']:
                return HttpResponse(403).error(ErrorCode.MAIL_NOK)
            # TODO voir pour faire choisir la method d'auth
            # TODO voir si le compte user créé par l'assistant permet aussi de se connecter normalement
            json_data = {
                'gender': 0,
                'lastname': 'lastname',
                'firstname': user_data['name'],
                'mail': user_data['email'],
                'password': 'password',
                'country': 'France',
                'town': 'Lille',
                'street': 'rue voltaire',
                'street_number': '1',
                'region': 'Hauts de france',
                'postal_code': '59000',
            }
            res = create_user(json_data)
            # modify object to respond to google
            if res['error'] is None:
                del res['error']
                del res['id']
                res['token_type'] = 'Bearer'
                res['access_token'] = res['access_token']
                res['refresh_token'] = res['refresh_token']
                return HttpResponse(200).custom(res)
            else:
                return HttpResponse(500).error(ErrorCode.UNK)
        if self.grant_type == 'authorization_code':
            (token, refresh_token) = self.grant_authorization_code()
        elif self.grant_type == 'refresh_token':
            (token, refresh_token) = self.grant_refresh_token()
        elif self.grant_type == 'password':
            (token, refresh_token) = self.grant_password()
        context = self.get_response_dict(token, refresh_token)
        return HttpResponse(200).custom(context)