from Ressources.swagger_api import api
from flask_restplus import fields

token_param = api.parser()
token_param.add_argument('client_id')
token_param.add_argument('client_secret')
token_param.add_argument('grant_type')
token_param.add_argument('code')
token_param.add_argument('refresh_token')


token_input = api.model('template_input', {
    'client_id': fields.Integer(example='f87b45e163a940a5a94b3cc33fb4e931', description="id de l'app"),
    'client_secret': fields.String(example='f87b45e163a940a5a94b3cc33fb4e931', description="client secret de l'app"),
    'grant_type': fields.String(example='password', description='methode utiliser pour récupérer le token'),
    'app-id': fields.String(example='arlex-ccevqe', description="nom de l'app qui essaye de récupérer un token"),
    'username': fields.String(example='test@arlex.com', description="mail pour identifier l'utilisateur"),
    'password': fields.String(example='password', description="password pour identifier l'utilisateur")
})
