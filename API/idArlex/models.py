from Ressources.swagger_api import api
from flask_restplus import fields

id_arlex_input = api.model('template_input', {
    'patch_id': fields.String(example='15151-AZDAZD-515451', description='Id du patch'),
})
