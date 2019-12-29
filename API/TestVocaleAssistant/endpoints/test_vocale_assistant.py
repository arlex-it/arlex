from flask import request
from flask_restplus import Resource
from Ressources.swagger_api import api
from API.TestVocaleAssistant.business import get_test_vocale_assistant
from API.TestVocaleAssistant.models import test_vocale_assistant_input

ns = api.namespace('test_vocale_assistant', description='Test if vocale assistant are up or down')


@ns.route('/')
class TestVocaleAssistantCollection(Resource):
    @ns.expect(test_vocale_assistant_input)
    @ns.response(200, '{"res": True}')
    def get(self):
        """
        This is a test route
        """
        print("Ouix")
        return get_test_vocale_assistant(request)