from API.Utilities.ErrorEnum import *
from API.Utilities.SuccesEnum import *
from flask import make_response, jsonify, render_template


class HttpResponse():
    def __init__(self, code=200):
        self.code = code

    def success(self, msg=SuccessCode.UNK, extra=None):
        succ = {
            'success': msg.value
        }
        if extra:
            succ['extra'] = extra
        return make_response(jsonify(succ), self.code)

    def error(self, msg=ErrorCode.UNK, exception: Exception = None):
        err = {
            'error': msg.value
        }
        if exception:
            err['message'] = exception.args
        return make_response(jsonify(err), self.code)

    def custom(self, dict):
        return make_response(jsonify(dict), self.code)
