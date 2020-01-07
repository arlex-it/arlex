import os
from urllib.parse import urlencode

import arrow
from flask import jsonify, render_template, make_response, redirect
from flask_restplus import abort
from flask_wtf import csrf

from API.Utilities import HttpRequestValidator
from API.Utilities.ErrorEnum import ErrorCode
from API.Utilities.HttpResponse import HttpResponse
from API.Utilities.SuccesEnum import SuccessCode
from API.User.business import check_password
from API.auth import OAuthRequestAbstract

from bdd.db_connection import session, User, Token


def get_auth(request):
    print(request)
    validator = HttpRequestValidator.HttpRequestValidator()
    if not request:
        abort(400)
    print(validator)
    validator.throw_on_error(enabled=False)
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
    # maybe shouldn't put id_project here
    #csrf.validate_csrf(request.form.get('csrf_token'))
    id_project = "arlex-ccevqe"
    # TODO créer une table AuthApp
    #app = self.get_app_with_client_id(client_id=request.values.get('client_id'))
    app = "google-assist-id"
    if id_project != request.form['redirect_uri'].rsplit('/', 1)[-1]:
        return HttpResponse(403).error(ErrorCode.BAD_TOKEN)
    if request.form['username']:
        # should be 'mail' and not 'username'
        user = session.query(User) \
            .join(Token, User.id == Token.id_user)\
            .filter(User.mail == request.form['username'])\
            .add_columns(User.id, User.password, Token.access_token)\
            .first()
        if user is None:
            # TODO sign-in user
            # voir si fonction yper recup arg request
            page = 'signin.html'
            # TODO how to redirect after signin ? In signin.html ?
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template(page,
                                                 client_id=request.values.get('client_id'),
                                                 redirect_uri=request.values.get('redirect_uri'),
                                                 state=request.values.get('state'),
                                                 response_type=request.values.get('response_type'),
                                                 scope=request.values.get('scope'),
                                                 year=arrow.now().format('YYYY')
                                                 ), 200, headers)
        elif check_password(request.form['password'], user.password.encode()):
            oauth_abstract = OAuthRequestAbstract.OAuthRequestAbstract()
            code = oauth_abstract.create_authorization_code(app)
            args = {
                "code": "testt",
                "state": request.form.get('state')
            }
            base_uri = request.form.get('redirect_uri')
            params = urlencode(args)
            url = f"{base_uri}?{params}"
            return redirect(url, code=302)


