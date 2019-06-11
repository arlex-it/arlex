from flask import request
from werkzeug.exceptions import BadRequest

from Tasker.helpers.generic import sub_key

class HTTPRequest(object):

    __request = None

    def __init__(self):
        self.__request = request

    def get_all_query_params(self):
        """
        Get all query params for a request

        :return: Dict of all query params
        """
        if self.__request and hasattr(self.__request, 'args'):
            return self.__request.args

        return {}

    def get_query_param(self, name, default=None):
        """
        Get a specific query parameter from request.

        :rtype: ImmutableMultiDict or None
        """
        if self.__request and hasattr(self.__request, 'args') and self.__request.args:
            return self.__request.args.get(name, default)

        return default

    def get_form_param(self, name, default=None):
        """
        Get a specific form paramter from request.

        :rtype: ImmutableMultiDict or None
        """
        if self.__request and hasattr(self.__request, 'form') and self.__request.form:
            return self.__request.form.get(name, default)

        return default

    def get_json_param(self, name, default=None):
        """
        Get the json payload from request.

        :rtype: * or None
        """
        if self.__request:

            try:
                json = self.__request.get_json(silent=True)
            except BadRequest:
                return default

            return sub_key(dictionary=json, key=name, default=default)

        return default

    def get_file_param(self, name, default=None):
        """
        Get a specific files from request.

        :rtype: str or None
        """
        if self.__request and hasattr(self.__request, 'files') and self.__request.files:
            return self.__request.files.get(name, default)

        return default

    def get_param(self, name, default=None):
        """
        Try every get method and return the first working one.
        """
        res = self.get_query_param(name, default)
        if res != default:
            return res

        res = self.get_form_param(name, default)
        if res != default:
            return res

        res = self.get_json_param(name, default)
        if res != default:
            return res

        # Try file
        res = self.get_file_param(name, default)
        if res != default:
            return res

        return default


    def get_header(self, name, default=None):
        """
        Get a specific header from request.

        :rtype: str or None
        """
        if self.__request and hasattr(self.__request, 'headers') and self.__request.headers:
            headers = {k: v for k, v in self.__request.headers.items()}
            # We convert headers to dict because special values (like X-Request-Timestamp)
            # are not always correctly parsed and cannot be retreived
            return headers.get(name, default)

        return default


