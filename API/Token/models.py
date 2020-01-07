from Ressources.swagger_api import api
from flask_restplus import fields

token_param = api.parser()
token_param.add_argument('code')
token_param.add_argument('client_id')
token_param.add_argument('client_secret')
token_param.add_argument('redirect_uri')
token_param.add_argument('grant_type')


token_input = api.model('template_input', {
    'input_1': fields.Integer(example=42, description='Ce paramètre ne sert à rien'),
    'input_2': fields.String(example='foo', description='celui là non plus'),
})
