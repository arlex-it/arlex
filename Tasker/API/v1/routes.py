from flask import Blueprint
from flask_cors import CORS

from Tasker.API.core.authentication.routes import register_oauth_routes
from Tasker.API.v1.product.DeleteProduct import APIV1ProductDeleteProduct
from Tasker.API.v1.product.GetInfo import APIV1ProductGetInfo
from Tasker.API.v1.product.PostCreate import APIV1ProductPostCreate
from Tasker.API.v1.product.PutInfo import APIV1ProductPutInfo
from Tasker.API.v1.user.PostCreate import APIV1UserPostCreate
import logging


blueprint_v1 = Blueprint('v1', __name__, template_folder="../templates", url_prefix="")
register_oauth_routes(blueprint_v1)
logging.getLogger('flask_assistant').setLevel(logging.DEBUG)

###
# USER
###
blueprint_v1.add_url_rule('/user', methods=['POST'], view_func=APIV1UserPostCreate.view())
#blueprint_v1.add_url_rule('/user/exist', methods=['GET'], view_func=APIV1UserPostCreate.view())

###
# PRODUCT
###
blueprint_v1.add_url_rule('/product', methods=['POST'], view_func=APIV1ProductPostCreate.view())
blueprint_v1.add_url_rule('/product/info/<product:product>', methods=['GET'], view_func=APIV1ProductGetInfo.view())
blueprint_v1.add_url_rule('/product/<product:product>', methods=['DELETE'], view_func=APIV1ProductDeleteProduct.view())
blueprint_v1.add_url_rule('/product/<product:product>', methods=['PUT'], view_func=APIV1ProductPutInfo.view())
