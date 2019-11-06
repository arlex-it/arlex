import logging
import json
import time

from flask import Blueprint
from flask_ask import Ask, statement, question, session
from flask_assistant import Assistant, tell
from Tasker.controllers.ProductController import ProductController

assit_blueprint_v1 = Blueprint('assist', __name__, url_prefix='/assist')
ask_blueprint_v1 = Blueprint('alexa', __name__, url_prefix='/alexa')
assist = Assistant(blueprint=assit_blueprint_v1)
alexa = Ask(blueprint=ask_blueprint_v1)
#
# logging.getLogger('flask_assistant').setLevel(logging.DEBUG)
#
# @assist.action('Default Welcome Intent')
# def google_welcome_intent():
#     return tell("bonjour")
#
# @assist.action('productCount')
# def google_objets_count(productcount):
#     product_ctrl = ProductController()
#     nbrProduct = product_ctrl.CountNbrOfProduct()
#     return tell(f'{nbrProduct} produits')
#
@alexa.launch
def start_skill():
    return question("Oui ?")

@alexa.intent('productCount')
def alexa_product_count():
    product_ctrl = ProductController()
    nbrProduct = product_ctrl.CountNbrOfProduct()
    # headlines = get_headlines()
    # headlines_msg= 'The current world news headliens are {}'.format(headlines)
    return statement(f'{nbrProduct} produits')