from Ressources.swagger_api import api
from flask_restplus import fields

products_create = api.model('Product create', {
    'expiration_date': fields.DateTime(example='2019-11-30 00:00:00', description='Date expiration produit'),
    'id_rfid': fields.Integer(example=567, description='Id du patch RFID du produit', required=True),
    'id_ean': fields.Integer(example=234, description='EAN du produit', required=True),
    'position': fields.String(example='placard sous evier', description='Endroit où est le produit'),
})