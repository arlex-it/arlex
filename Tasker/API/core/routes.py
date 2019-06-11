"""
Base route, blueprint and converter registration.
"""
import os
import socket
from Tasker.API.core.HTTPReponse import HTTPResponse
from Tasker.helpers.generic import load_config
from Tasker.API.common.converters import (UserConverter)
from Tasker.API.v1.routes import blueprint_v1

dir_path = os.path.dirname(os.path.realpath(__file__))

config = load_config()

def register_routes(app):
    @app.route("/")
    def base():
        return HTTPResponse(200, {'hostname': socket.gethostname(), 'build': config['build']}).get_response()

    app.url_map.converters['user'] = UserConverter

    app.register_blueprint(blueprint_v1)