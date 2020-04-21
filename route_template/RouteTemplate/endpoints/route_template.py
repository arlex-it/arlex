from flask import request
from flask_restplus import Resource
from Ressources.swagger_api import api
from API.RouteTemplateBusiness.business import get_route_template
from API.RouteTemplateModels.models import route_template_input

ns = api.namespace('template_namespace', description='template_description')


@ns.route('/')
class TemplateCollection(Resource):
    @ns.expect(route_template_input)
    @ns.response(200, '{"res": True}')
    def post(self):
        """
        This is a test route
        """
        return get_route_template(request)
