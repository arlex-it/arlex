from Ressources.swagger_api import api
from flask_restplus import fields

auth_authorize_param = api.parser()
auth_authorize_param.add_argument('redirect_uri', location='path')
auth_authorize_param.add_argument('response_type', location='path', default='code')
auth_authorize_param.add_argument('state', location='path')
auth_authorize_param.add_argument('user_locale', location='path')
auth_authorize_param.add_argument('client_id', location='path')

post_auth_model = api.parser()
post_auth_model.add_argument('client_id', location='path')
post_auth_model.add_argument('response_type', location='path')
post_auth_model.add_argument('redirect_uri', location='path')
post_auth_model.add_argument('username', location='path')
post_auth_model.add_argument('password', location='path')
