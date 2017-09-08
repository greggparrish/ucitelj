from .base import *

DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['UCITELJ_DB_NAME'],
        'USER': os.environ['UCITELJ_DB_USER'],
        'PASSWORD': os.environ['UCITELJ_DB_KEY'],
        'HOST': 'localhost',
        'PORT': '',
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions',
)
MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
INTERNAL_IPS = ('127.0.0.1',)
