from flask import request

class HttpRequest(object):

    __request = None

    def __init__(self):
        self.__request = request

    def get_header(self, name, default=None):
        """
        Get a specific header from request.

        :rtype: str or None
        """
        if self.__request and hasattr(self.__request, 'headers') and self.__request.headers:
            headers = {k: v for k, v in self.__request.headers.items()}
            # We convert headers to dict because special values (like X-Request-Timestamp)
            # are not always correctly parsed and cannot be retreived
            # https://mail.python.org/pipermail/flask/2017-July/000888.html
            return headers.get(name, default)

        return default