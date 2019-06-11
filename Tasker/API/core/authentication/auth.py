"""
Authentification methods.
"""
import re

from Tasker.API.core.HTTPRequest import HTTPRequest
from Tasker.helpers.exceptions import BadRequest, ForbiddenError, UnauthorizedError
from Tasker.helpers.OAuthAuthenticationHelper import OAuthAuthenticationTokenHelper

TYPE_PRIVATE = 'private'
TYPE_PUBLIC = 'public_authenticated'

def private_authentication(scopes, kwargs):
    """
    :rtype: bool
    """
    request = HTTPRequest()
    token = request.get_param('oauth_access_token')
    timestamp = request.get_param('oauth_timestamp')

    header_token = request.get_header("Authorization")
    if header_token:
        reg = re.compile('Bearer ([A-Za-z0-9-_=]+)')
        result = reg.findall(header_token)
        if result:
            token = result[0]

    header_timestamp = request.get_header('X-Request-Timestamp')
    if header_timestamp:
        timestamp = header_timestamp

    if not token:
        raise UnauthorizedError('No oauth_access_token or Authorization header found in request')

    if not timestamp:
        raise BadRequest('No oauth_timestamp or X-Request-Timestamp found in request')

    helper = OAuthAuthenticationTokenHelper(token)

    if not helper.is_valid_token():
        raise UnauthorizedError('Invalid access token')
    if not helper.has_scopes(scopes):
        raise ForbiddenError('Access token has insufficient scope')
    if helper.has_entity():
        # Excluding client_credentials grant
        if not helper.validate_models(kwargs):
            raise ForbiddenError('Unmatched model entities')
    return helper.get_token_infos()


def public_authentication(scopes):
    """
    :rtype: bool
    """
    return True


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

            kwargs.update({'oauth_token': infos})

            response = func(*args, **kwargs)
            return response
        return wrapper
    return decorated