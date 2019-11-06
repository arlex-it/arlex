from Tasker.API.v1 import AbstractView
from Tasker.API.assist_v1.routes import assist
from Tasker.controllers.ProductController import ProductController
from flask_assistant import tell, request
from Tasker.API.core.HTTPReponse import HTTPResponse


class APIV1ProductGetInfo(AbstractView):
    @assist.action('productCount')
    def dispatch_request(self, **kwargs):
        try:
            request['queryResult']
        except:
            product_ctrl = ProductController()
            nbrProduct = product_ctrl.CountNbrOfProduct()
            return HTTPResponse(200, {}).get_response()
        product_ctrl = ProductController()
        nbrProduct = product_ctrl.CountNbrOfProduct()
        return tell(f'{nbrProduct} produits')