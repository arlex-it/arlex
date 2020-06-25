from flask import url_for
from flask_restplus import Api
from Ressources import settings


class CustomAPI(Api):
    @property
    def specs_url(self):
        """
        The Swagger specifications absolute url (ie. `swagger.json`)

        :rtype: str
        """
        return url_for(self.endpoint('specs'), _external=False)


api = CustomAPI(version='1.0', title='Arlex API', description='API for Arlex Project')


@api.errorhandler
def default_error_handler():
    message = 'An unhandled exception occurred.'
    if not settings.FLASK_DEBUG:
        return {'message': message}, 500
