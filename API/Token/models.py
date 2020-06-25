from Ressources.swagger_api import api
from flask_restplus import fields

token_param = api.parser()
token_param.add_argument('client_id')
token_param.add_argument('client_secret')
token_param.add_argument('grant_type')
token_param.add_argument('code')
token_param.add_argument('refresh_token')