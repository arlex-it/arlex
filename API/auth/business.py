import os
import arrow
from flask import jsonify, render_template, make_response
from flask_restplus import abort

from API.Utilities import HttpRequestValidator
from API.Utilities.ErrorEnum import ErrorCode
from API.Utilities.HttpResponse import HttpResponse
from API.Utilities.SuccesEnum import SuccessCode


def get_auth(request):
    print(request)
    validator = HttpRequestValidator.HttpRequestValidator()
    if not request:
        abort(400)
    print(validator)
    validator.throw_on_error(enabled=False)
    validator.add_param('response_type', location=HttpRequestValidator.Location.query)

    validator.add_param('response_type', location=HttpRequestValidator.Location.query)
    validator.add_param('client_id', location=HttpRequestValidator.Location.query)
    validator.add_param('redirect_uri', location=HttpRequestValidator.Location.query)
    validator.add_param('state', location=HttpRequestValidator.Location.query)
    if not validator.verify():
        return HttpResponse().error(ErrorCode.UNK)

    response_type = request.values.get('response_type')

    if response_type != 'code':
        raise Exception('Unsupported response_type')

    client_id=request.values.get('client_id')

    scope = request.values.get('scope')
    if scope is not None:
        scopes = scope.split(',')

    print(os.getcwd())
    page = 'authorize.html'
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template(page,
                                         client_id=request.values.get('client_id'),
                                         redirect_uri=request.values.get('redirect_uri'),
                                         state=request.values.get('state'),
                                         response_type=request.values.get('response_type'),
                                         scope=request.values.get('scope'),
                                         year=arrow.now().format('YYYY')
                                         ), 200, headers)


def post_auth(request):
    pass

def post_token(request):
    return HttpResponse(201).success(SuccessCode.USER_CREATED, {"token_type": "Bearer", "access_token": "tokeennnn", "expires_in": "09889786655"})