#!env/bin/python

from flask import Flask, Blueprint, request, jsonify
from Ressources import settings
from Ressources.config import configure_app
from Ressources.swagger_api import api
from API.Test.enpoints.test import ns as test_namespace
from API.Products.endpoints.products import ns as products
import bdd.db_connection
# Template import marker

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def description():
	"""
	Description of the API
	"""
	return jsonify({'Description': 'Arlex API !', 'Documentation': request.url + 'api/'})


def initialize_app(flask_app):
	configure_app(flask_app)
	blueprint = Blueprint('api', __name__, url_prefix='/api')
	api.init_app(blueprint)
	api.add_namespace(test_namespace)
	api.add_namespace(products)
	# Template namespace marker
	flask_app.register_blueprint(blueprint)


def launcher():
	initialize_app(app)
	app.run(debug=settings.FLASK_DEBUG, port=5000, host='0.0.0.0')


def wsgi_launcher():
	initialize_app(app)


if __name__ == '__main__':
	launcher()
else:
	wsgi_launcher()
