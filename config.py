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
    ADMIN_EMAIL='me@greggparrish.com'

    CSRF_ENABLED = True
    DEBUG = False
    TESTING = False

    MAIL_USERNAME = os.environ.get('UCITELJ_MAIL_USER')
    MAIL_PASSWORD = os.environ.get('UCITELJ_MAIL_PASS')
    MAIL_DEFAULT_SENDER = '"Sender" <noreply@greggparrish.com>'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False

    USER_UNAUTHORIZED_ENDPOINT = '/'
    USER_LOGIN_TEMPLATE = 'users/login.html'
    USER_REGISTER_TEMPLATE = 'users/register.html'

    UPLOADS_DEFAULT_DEST = 'app/static/public/uploads/'
    UPLOADS_DEFAULT_URL = '/static/public/uploads/'
    UPLOADS_IMAGE_DEST = 'app/static/public/uploads/images/'
    UPLOADS_IMAGE_URL = '/static/public/uploads/images/'


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestConfig(Config):
    TESTING = True
