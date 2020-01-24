from Ressources.swagger_api import api
from flask_restplus import fields

products_create = api.model('Product create', {
    'expiration_date': fields.DateTime(example='2019-11-30', description='Date expiration produit', required=True),
    'id_rfid': fields.Integer(example=567, description='Id du patch RFID du produit', required=True),
    'id_ean': fields.String(example='3017620424403', description='EAN du produit', required=True),
    'position': fields.String(example='placard sous evier', description='Endroit où est le produit', required=True),
})