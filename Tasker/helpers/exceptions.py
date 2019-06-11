"""
Arlex Tasker exceptions.
"""


class ArlexException(Exception):

    _code = 500  # value if converted as http status code
    _scope = 'arlex_error'  # scope of the error (error_code)
    _prefix = ''  # string to put before the error message

    def __init__(self, message, scope=None, code=None):
        self.scope = scope or self._scope
        self.description = f'{self._prefix}{message}'
        self.code = code or self._code

class ConverterError(ArlexException):
    """
    Generic Converter error.
    """
    _scope = 'converter_error'

class InvalidParameter(ArlexException):
    """
    Invalid parameter error.
    """
    _scope = 'invalid_parameter'

class InvalidValue(ArlexException):
    """
    Invalid value error.
    """
    _scope = 'invalid_value'


class ModelError(ArlexException):
    """
    Generic Model error.
    """
    _scope = 'model_error'

# ===== API errors =====

class AuthError(ArlexException):
    """
    Failed to authenticate.
    """
    _code = 400
    _scope = 'invalid_credentials'


class BadRequest(ArlexException):
    """
    Mark a malformed requests.
    """
    _code = 400
    _scope = 'invalid_request'

class ForbiddenError(ArlexException):
    """
    Forbidden to access at this resource.
    """
    _code = 403
    _scope = 'invalid_access'

class UnauthorizedError(ArlexException):
    """
    Cannot have sufficient authorizations.
    """
    _code = 401
    _scope = 'invalid_access'



# ===== Specific errors =====

class InvalidApplication(ArlexException):
    """
    Invalid application error.
    """
    _code = 400
    _scope = 'invalid_application'

# ===== Generic errors =====

class ControllerError(ArlexException):
    """
    Generic Controller error.
    """
    _scope = 'controller_error'

