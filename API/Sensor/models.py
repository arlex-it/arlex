from Ressources.swagger_api import api
from flask_restplus import fields

sensor_input = api.parser()
sensor_input.add_argument('id', type=int, help="User ID", required=True)
