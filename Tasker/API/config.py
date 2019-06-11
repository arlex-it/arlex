"""
Available configurations for flask app.
"""


class Config(object):
    DEBUG = False
    TESTING = False
    WTF_CSRF_CHECK_DEFAULT = False
    SECRET_KEY = 'SECRET_KEY'


class ProductionConfig(Config):
    DEBUG = False
    JSONIFY_PRETTYPRINT_REGULAR = False


class DevelopmentConfig(Config):
    DEBUG = True
    JSONIFY_PRETTYPRINT_REGULAR = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False