from Tasker.helpers.exceptions import ControllerError
from Tasker.models.ProductModel import ProductModel
from Tasker.controllers.AbstractController import AbstractController

class ProductController(AbstractController):
    def CountNbrOfProduct(self):
        products = ProductModel.objects().all()
        nbrProduct = len(products)
        return nbrProduct