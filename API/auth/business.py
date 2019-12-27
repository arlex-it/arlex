from flask import jsonify
from flask_restplus import abort

from API.Utilities import HttpRequestValidator
from API.Utilities.ErrorEnum import ErrorCode
from API.Utilities.HttpResponse import HttpResponse
from API.Utilities.SuccesEnum import SuccessCode


def get_auth(request):
    validator = HttpRequestValidator.HttpRequestValidator()
    if not request:
        abort(400)
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

    return(f'https://oauth-redirect.googleusercontent.com/r/YOUR_PROJECT_ID=arlex-ccevqe?code=test&state={request.values.get("state")}')


def post_token(request):
    return HttpResponse(201).success(SuccessCode.USER_CREATED, {"token_type": "Bearer", "access_token": "tokeennnn", "expires_in": "09889786655"})