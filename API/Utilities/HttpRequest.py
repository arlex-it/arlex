from flask import request

from werkzeug.exceptions import BadRequest

from API.Utilities.generic import sub_key


class HttpRequest(object):

    request = None

    def __init__(self):
        self.request = request

    def get_header(self, name, default=None):
        """
        Get a specific header from request.

        :rtype: str or None
        """
        if self.request and hasattr(self.request, 'headers') and self.request.headers:
            headers = {k: v for k, v in self.request.headers.items()}
            # We convert headers to dict because special values (like X-Request-Timestamp)
            # are not always correctly parsed and cannot be retreived
            # https://mail.python.org/pipermail/flask/2017-July/000888.html
            return headers.get(name, default)

        return default

    def get_query_param(self, name, default=None):
        """
        Get a specific query parameter from request.

        :rtype: ImmutableMultiDict or None
        """
        if self.request and hasattr(self.request, 'args') and self.request.args:
            return self.request.args.get(name, default)

        return default

    def get_form_param(self, name, default=None):
        """
        Get a specific form paramter from request.

        :rtype: ImmutableMultiDict or None
        """
        if self.request and hasattr(self.request, 'form') and self.request.form:
            return self.request.form.get(name, default)

        return default

    def get_json_param(self, name, default=None):
        """
        Get the json payload from request.

        :rtype: * or None
        """
        if self.request:

            try:
                json = self.request.get_json(silent=True)
            except BadRequest:
                return default

            return sub_key(dictionary=json, key=name, default=default)

        return default

    def get_file_param(self, name, default=None):
        """
        Get a specific files from request.

        :rtype: str or None
        """
        if self.request and hasattr(self.request, 'files') and self.request.files:
            return self.request.files.get(name, default)

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