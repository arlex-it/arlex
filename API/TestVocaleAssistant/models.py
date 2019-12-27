from Ressources.swagger_api import api
from flask_restplus import fields

test_vocale_assistant_input = api.model('template_input', {
    'input_1': fields.Integer(example=42, description='Ce paramètre ne sert à rien'),
    'input_2': fields.String(example='foo', description='celui là non plus'),
})
