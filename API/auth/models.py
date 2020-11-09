from Ressources.swagger_api import api
from flask_restplus import fields

auth_authorize_param = api.parser()
auth_authorize_param.add_argument('redirect_uri', location='path')
auth_authorize_param.add_argument('response_type', location='path', default='code')
auth_authorize_param.add_argument('state', location='path')
auth_authorize_param.add_argument('user_locale', location='path')
auth_authorize_param.add_argument('client_id', location='path')

post_auth_model = api.model('Post auth', {
    'client_id': fields.Integer(example=0, required=True),
    'response_type': fields.String(example='code', description='Type de réponse', required=True),
    'redirect_uri': fields.String(example='https://redirect_url', required=True),
    'username': fields.String(example='john@doe.com', description='Adresse mail de l\'utilisateur', required=True),
    'password': fields.String(example='password', description='Mot de passe de l\'utilisateur', required=True),
})
