from Ressources.swagger_api import api
from flask_restplus import fields

getweather_input = api.model('getweather_input', {
    'city': fields.String(example='London', description='City name'),
})
