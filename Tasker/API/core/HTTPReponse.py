#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import make_response, jsonify
from Tasker.helpers.exceptions import ArlexException

INVALID_FIELD_NAME_SENT_422 = {
    "http_code": 422,
    "code": "invalidField",
    "message": "Not all field names are valid."
}

INVALID_INPUT_422 = {
    "http_code": 422,
    "code": "invalidInput",
    "message": "Invalid input"
}

MISSING_PARAMETERS_422 = {
    "http_code": 422,
    "code": "missingParameter",
    "message": "Missing parameters."
}

BAD_REQUEST_400 = {
    "http_code": 400,
    "code": "badRequest",
    "message": "Bad request"
}

SERVER_ERROR_500 = {
    "http_code": 500,
    "code": "serverError",
    "message": "Server error"
}

SERVER_ERROR_404 = {
    "http_code": 404,
    "code": "notFound",
    "message": "Resource not found"
}

UNAUTHORIZED_403 = {
    "http_code": 403,
    "code": "notAuthorized",
    "message": "You are not allowed to do that."
}

NOT_FOUND_HANDLER_404 = {
    "http_code": 404,
    "code": "notFound",
    "message": "There are no such handler"
}

TOO_MANY_REQUESTS_429 = {
    "http_code": 429,
    "code": "tooManyRequest",
    "message": "Too many requests"
}

SUCCESS_200 = {
    'http_code': 200,
    'code': 'success'
}

class HTTPResponse(object):
    """
    Generic HTTP Response class.
    """

    __code = 200
    __headers = {}
    __content = {}

    __error = False
    __error_code = ""
    __error_message = ""
    __error_display_message = ""

    def __init__(self, status_code=200, context={}, headers={}):
        self.__code = status_code
        self.__content = context
        self.__headers = headers

        self.__error = False
        self.__error_code = ""
        self.__error_message = ""
        self.__error_display_message = ""

        self.disable_cache()

    def disable_cache(self):
        self.__headers.update({
            'Cache-Control': 'no-store'
        })
        return self

    def set_status_code(self, code):
        self.__code = code
        return self

    def set_content(self, content):
        self.__content = content
        return self

    def set_error(self, error):
        self.__error = True

        if issubclass(type(error), ArlexException):
            # Branch for standarized exception system
            self.set_status_code(error.code)
            self.__error_code = error.scope
            self.__error_message = error.description
            return

        # Default error
        self.__error_code = None
        self.set_status_code(500)
        self.__error_code = "internal_server_error"
        self.__error_message = "500: Internal Server Error"

        if hasattr(error, "code"):
            self.set_status_code(error.code)

        if hasattr(error, "error_code"):
            self.__error_code = error.error_code

        if hasattr(error, "error_display_message"):
            self.__error_display_message = error.error_display_message

        if hasattr(error, "description"):
            self.__error_message = error.description

    def get_response(self):
        """
        :rtype: flask.Response
        """
        self.__headers.update({'Access-Control-Allow-Origin': '*'})
        self.__headers.update({'Server': 'arlex.io v1.0'})

        if not self.__error:
            response = {
                "status": self.__code,
                "result": self.__content
            }
        else:
            response = {
                "status": self.__code,
                "error_code": self.__error_code,
                "error_message": self.__error_message
            }

            if self.__error_display_message:
                response.update({'error_display_message': self.__error_display_message})

        return make_response(jsonify(response), self.__code, self.__headers)