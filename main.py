#!env/bin/python
import os
import uuid

from flask import Flask, Blueprint, request, jsonify
from Ressources import settings
from Ressources.config import configure_app
from Ressources.swagger_api import api
from API.Test.enpoints.test import ns as test_namespace
from API.User.endpoints.user import ns as user
from API.TestVocaleAssistant.endpoints.test_vocale_assistant import ns as test_vocale_assistant
import bdd.db_connection
from API.auth.endpoints.auth import ns as auth
from API.Token.endpoints.token import ns as token
# templates import marker

app = Flask(__name__, template_folder="API/templates/")
# Template import marker
app.url_map.strict_slashes = False


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def description():
	"""
	Description of the API
	"""
	return jsonify({'Description': 'Arlex API !', 'Documentation': request.url + 'api/'})


def initialize_app(flask_app):
	access_token = uuid.uuid4().hex[:35]
	#CSRFProtect(app)
	configure_app(flask_app)
	blueprint = Blueprint('api', __name__, url_prefix='/api', template_folder='API/templates/')
	api.init_app(blueprint)
	api.add_namespace(test_namespace)
	api.add_namespace(auth)
	api.add_namespace(token)
	api.add_namespace(test_vocale_assistant)
	# templates namespace marker
	flask_app.register_blueprint(blueprint)


def launcher():
	initialize_app(app)
	use_reloader=True
	app.run(debug=settings.FLASK_DEBUG, port=5000, host='0.0.0.0', use_reloader=use_reloader)


def wsgi_launcher():
	initialize_app(app)


if __name__ == '__main__':
	launcher()
else:
	wsgi_launcher()
