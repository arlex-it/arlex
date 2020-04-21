from Ressources.swagger_api import api
from flask_restplus import fields

auth_authorize_param = api.parser()
auth_authorize_param.add_argument('redirect_uri', location='path')
auth_authorize_param.add_argument('response_type', location='path')
auth_authorize_param.add_argument('state', location='path')
auth_authorize_param.add_argument('user_locale', location='path')
auth_authorize_param.add_argument('client_id', location='path')

auth_input = api.model('template_input', {
    'input_1': fields.Integer(example=42, description='Ce paramètre ne sert à rien'),
    'input_2': fields.String(example='foo', description='celui là non plus'),
})
