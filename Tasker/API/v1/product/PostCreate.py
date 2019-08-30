from Tasker.API.core.HTTPReponse import HTTPResponse
from Tasker.API.v1 import AbstractView
from Tasker.controllers.UserController import UserController
from flask import g

from Tasker.models.ProductModel import ProductModel


class APIV1ProductPostCreate(AbstractView):
    def __init__(self):
        self.product_model = ProductModel()
    def dispatch_request(self, **kwargs):
        product = self.product_model.create(
            product_name=g.data['product_name'],
            wardrobe=g.data['wardrobe'],
            stage=g.data['stage'],
            expiration_date=g.data['expiration_date']
        )
        response = HTTPResponse(200).set_content(product.id)
        return response.get_response()