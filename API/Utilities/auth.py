"""
Authentification methods.
"""

import re

from werkzeug.exceptions import BadRequest

from API.Utilities.HttpRequest import HttpRequest
from API.Utilities.OAuthAuthenticationToken import OAuthAuthenticationToken
from bdd.db_connection import session, AccessToken, to_dict

TYPE_PRIVATE = 'private'
TYPE_PUBLIC = 'public_authenticated'


def check_user_permission(user_id):
    requester = HttpRequest()

    token = requester.get_param('accessToken')
    timestamp = requester.get_param('oauth_timestamp')
    header_token = requester.get_header("Authorization")

    if header_token is None:
        header_token = requester.get_header("X-Authorization")

    if header_token:
        reg = re.compile('Bearer ([A-Za-z0-9-_=]+)')
        result = reg.findall(header_token)
        if result:
            token = result[0]

    user_connected = session.query(AccessToken).filter(AccessToken.token == token).first()
    user_connected = to_dict(user_connected)
    if int(user_connected['id_user']) != int(user_id):
        return False
    return True

def public_authentication(scopes):
    """
    :rtype: bool
    """
    return True


def private_authentication(scopes, kwargs):
    request = HttpRequest()
    token = request.get_param('accessToken')
    timestamp = request.get_param('oauth_timestamp')
    header_token = request.get_header("Authorization")
    
    if header_token is None:
        header_token = request.get_header("X-Authorization")

    if header_token:
        reg = re.compile('Bearer ([A-Za-z0-9-_=]+)')
        result = reg.findall(header_token)
        if result:
            token = result[0]

    header_timestamp = request.get_header('X-Request-Timestamp')
    if header_timestamp:
        timestamp = header_timestamp

    if not token:
        raise Exception('No oauth_access_token or Authorization header found in request')
    helper = OAuthAuthenticationToken(token)
    if not helper.is_valid_token():
        raise Exception('Invalid access token')

    # TODO SCOPE
    if not helper.has_scopes([scopes]):
        raise Exception('Access token has insufficient scope')
    return helper.get_token_infos()


def require_authentication(type_, scopes=[]):
    """
    Decorator for routes authentification.
    :param str type_: is it a private or a public route ?
    :param list scopes: scopes need to access this route
    """
    def decorated(func):
        def wrapper(*args, **kwargs):
            if type_ == TYPE_PRIVATE:
                infos = private_authentication(scopes, kwargs)
            elif type_ == TYPE_PUBLIC:
                infos = public_authentication(scopes)
            else:
                raise BadRequest('The requested authentication method does not exists')
            response = func(*args, **kwargs)
            return response
        return wrapper
    return decorated