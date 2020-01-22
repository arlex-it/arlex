import arrow
from flask import make_response, render_template
from flask_restplus import abort

from API.Utilities import HttpRequestValidator
from API.Utilities.HttpResponse import HttpResponse, ErrorCode
from API.auth.OAuthRequestAbstract import OAuthRequestAbstract

class GetAuthorization(OAuthRequestAbstract):

    def dispatch_request(self, request):
        validator = HttpRequestValidator.HttpRequestValidator()
        if not request:
            abort(400)
        validator.throw_on_error(enabled=False)
        validator.add_param('response_type', location=HttpRequestValidator.Location.query)
        validator.add_param('client_id', location=HttpRequestValidator.Location.query)
        validator.add_param('redirect_uri', location=HttpRequestValidator.Location.query)
        validator.add_param('state', location=HttpRequestValidator.Location.query)
        if not validator.verify():
            return HttpResponse().error(ErrorCode.UNK)

        response_type = request.values.get('response_type')

        app = self.get_app_with_client_id(client_id=request.values.get('client_id'))

        if response_type != 'code':
            raise Exception('Unsupported response_type')

        page = 'authorize.html'
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template(page,
                                             app=app.app_name,
                                             client_id=request.values.get('client_id'),
                                             redirect_uri=request.values.get('redirect_uri'),
                                             state=request.values.get('state'),
                                             response_type=request.values.get('response_type'),
                                             year=arrow.now().format('YYYY')
                                             ), 200, headers)