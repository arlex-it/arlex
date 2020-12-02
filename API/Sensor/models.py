from Ressources.swagger_api import api
from flask_restplus import fields

sensor_get_list_product = api.parser()
sensor_get_list_product.add_argument('Authorization')

sensor_post_product = api.parser()
sensor_post_product.add_argument('Authorization')

sensor_get_position = api.parser()
sensor_get_position.add_argument('Authorization')
sensor_get_position.add_argument('product_name', required=True)

sensor_rename = api.parser()
sensor_rename.add_argument('Authorization')
sensor_rename.add_argument('old_name', required=True)
sensor_rename.add_argument('new_name', required=True)

link_sensor_post = api.parser()
link_sensor_post.add_argument('Authorization')

name_sensor = api.parser()
name_sensor.add_argument('Authorization')

sensor_list = api.parser()
sensor_list.add_argument('Authorization')