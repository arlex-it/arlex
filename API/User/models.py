from Ressources.swagger_api import api
from flask_restplus import fields


user_get = api.parser()
user_get.add_argument('mail', type=str, help="john@doe.com", required=True)

user_creation = api.model('User creation', {
    'gender': fields.Integer(example=0, description='Genre de l\'utilisateur', required=True),
    'lastname': fields.String(example='Doe', description='Nom de l\'utilisateur', required=True),
    'firstname': fields.String(example='John', description='Prenom de l\'utilisateur', required=True),
    'mail': fields.String(example='john@doe.com', description='Adresse mail de l\'utilisateur', required=True),
    'password': fields.String(example='password', description='Mot de passe de l\'utilisateur', required=True),
    'country': fields.String(example='France', description='Pays de l\'utilisateur', required=True),
    'town': fields.String(example='Lille', description='Ville de l\'utilisateur', required=True),
    'street': fields.String(example='rue nationale', description='Rue de l\'utilisateur', required=True),
    'street_number': fields.String(example='13', description='Numéro de rue de l\'utilisateur', required=True),
    'region': fields.String(example='Hauts de france', description='Région de l\'utilisateur', required=True),
    'postal_code': fields.String(example="12345", description='Code postal de l\'utilisateur', required=True),
})

user_update_header = api.parser()
user_update_header.add_argument('Authorization', type=str, help="Bearer Token", location='headers', required=True)

user_update = api.model('User update', {
    'gender': fields.Integer(example=0, description='Nouveau Genre de l\'utilisateur'),
    'lastname': fields.String(example='Doe', description='Nouveau Nom de l\'utilisateur'),
    'firstname': fields.String(example='John', description='Nouveau Prenom de l\'utilisateur'),
    'mail': fields.String(example='john@doe.com', description='Nouvelle Adresse mail de l\'utilisateur'),
    'password': fields.String(example='password', description='Nouveau Mot de passe de l\'utilisateur'),
    'country': fields.String(example='France', description='Nouveau Pays de l\'utilisateur'),
    'town': fields.String(example='Lille', description='Nouvelle Ville de l\'utilisateur'),
    'street': fields.String(example='rue nationale', description='Nouvelle Rue de l\'utilisateur'),
    'street_number': fields.String(example='13', description='Nouveau Numéro de rue de l\'utilisateur'),
    'region': fields.String(example='Hauts de france', description='Nouvelle  Région de l\'utilisateur'),
    'postal_code': fields.String(example="12345", description='Nouveau Code postal de l\'utilisateur'),
})
