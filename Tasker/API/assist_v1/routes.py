import logging

from flask import Blueprint
from flask_assistant import Assistant, ask, tell
from Tasker.controllers.ProductController import ProductController

assit_blueprint_v1 = Blueprint('assist', __name__, url_prefix='/assist')
assist = Assistant(blueprint=assit_blueprint_v1)

logging.getLogger('flask_assistant').setLevel(logging.DEBUG)

@assist.action('productCount')
def google_objets_count(productCount):
    product_ctrl = ProductController()
    nbrProduct = product_ctrl.CountNbrOfProduct()
    return tell(f'{nbrProduct} produits')