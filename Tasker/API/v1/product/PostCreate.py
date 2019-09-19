from flask_expects_json import expects_json

from Tasker.API.core.HTTPReponse import HTTPResponse
from Tasker.API.v1 import AbstractView
from Tasker.controllers.UserController import UserController
from flask import g

from Tasker.models.ProductModel import ProductModel

SCHEMA = {
    'type': 'object',
    'properties': {
        'product_name': {'type': 'string'},
        'wardrobe': {'type': 'string'},
        'stage': {'type': 'string'},
        'expiration_date': {'type': 'string'},
    },
    'required': ['product_name', 'wardrobe', 'stage', 'expiration_date']
}

class APIV1ProductPostCreate(AbstractView):
    def __init__(self):
        self.product_model = ProductModel()

    @expects_json(SCHEMA)
    def dispatch_request(self, **kwargs):
        print("AHH")
        product = self.product_model.create(
            product_name=g.data['product_name'],
            wardrobe=g.data['wardrobe'],
            stage=g.data['stage'],
            expiration_date=g.data['expiration_date']
        )
        response = HTTPResponse(200).set_content(product.id)
        return response.get_response()