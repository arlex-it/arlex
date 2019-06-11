from flask import render_template

from Tasker.API.core import HTTPRequestValidator
from Tasker.API.core.authentication.OAuthRequestAbstract import OAuthRequestAbstract


class APICoreAuthenticationGetAuthorize(OAuthRequestAbstract):

    def dispatch_request(self, blueprint):
        """
        :param Blueprint blueprint: using blueprint to find out template folder.
        """
        validator = HTTPRequestValidator.HTTPRequestValidator()
        validator.throw_on_error(enabled=False)

        validator.add_param('response_type', location=HTTPRequestValidator.Location.query)
        validator.add_param('client_id', location=HTTPRequestValidator.Location.query)
        validator.add_param('redirect_uri', location=HTTPRequestValidator.Location.query)
        validator.add_param('state', location=HTTPRequestValidator.Location.query)

        if not validator.verify():
            return render_template('authorize-invalid.html')