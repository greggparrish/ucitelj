import os

class Config(object):
    SECRET_KEY = os.environ.get('UCITELJ_SECRET')

    """ DB SETTINGS """
    UCITELJ_DB = {
            'user': os.environ.get('UCITELJ_USER'),
            'pass': os.environ.get('UCITELJ_PASS'),
            'db': os.environ.get('UCITELJ_DB'),
            }
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pass)s@localhost:5432/%(db)s' % UCITELJ_DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CSRF_ENABLED = True
    DEBUG = False
    TESTING = False

class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestConfig(Config):
    TESTING = True
