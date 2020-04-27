from flask import request
from flask_restplus import Resource
from Ressources.swagger_api import api
from API.Test.business import get_test
from API.Test.models import test_input

ns = api.namespace('test', description='Test operations')


@ns.route('/')
class TestCollection(Resource):
    @ns.expect(test_input)
    @ns.response(200, '{"res": True}')
    def post(self):
        """
        This is a test route
        """
        return get_test(request)
