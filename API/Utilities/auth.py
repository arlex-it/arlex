"""
Authentification methods.
"""

import re

from werkzeug.exceptions import BadRequest

from API.Utilities.HttpRequest import HttpRequest

TYPE_PRIVATE = 'private'
TYPE_PUBLIC = 'public_authenticated'

def public_authentication(scopes):
    """
    :rtype: bool
    """
    return True

def private_authentication(scopes, kwargs):
    request = HttpRequest()
    header_token = request.get_header("Authorization")
    print(header_token)

def require_authentication(type_, scopes=[]):
    """
    Decorator for routes authentification.

    :param str type_: is it a private or a public route ?
    :param list scopes: scopes need to access this route
    """
    def decorated(func):
        def wrapper(*args, **kwargs):
            print(scopes)
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