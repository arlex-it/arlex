from Ressources import settings


def configure_app(flask):
    flask.config['SECRET_KEY'] = 'SECRET_KEY'
    flask.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
