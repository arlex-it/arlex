#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import traceback
from flask import Flask
from Tasker.helpers.CoreHelper import CoreHelper
from werkzeug.exceptions import default_exceptions
from Tasker.API.core.HTTPReponse import HTTPResponse
from Tasker.API.core.routes import register_routes

def make_json_error(ex):
    logging.error(ex)

    res = HTTPResponse()
    res.set_error(ex)

    traceback.print_exc()

    return res.get_response()

def create_app(config):
    app = Flask(__name__, template_folder="../templates/", static_folder="../static")
    app._static_folder = "../static"

    for code in default_exceptions:
        app.register_error_handler(code_or_exception=code, f=make_json_error)
    CoreHelper.mongodb_connect()

    register_routes(app)
    return app

