from Ressources.swagger_api import api
from flask_restplus import fields

product_update_header = api.parser()
product_update_header.add_argument('Authorization', type=str, help="Bearer Token", location='headers', required=True)
product_authorization_header = api.parser()
product_authorization_header.add_argument('Authorization', type=str, help="Bearer Token", location='headers', required=True)