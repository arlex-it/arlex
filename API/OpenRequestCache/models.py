from Ressources.swagger_api import api
from flask_restplus import fields

open_request_cache_input = api.model('open_request_cache_input', {
    'url': fields.String(example='https://fr.openfoodfacts.org/produit/3222473310661', description='Url openfoodfact', required=True),
})
