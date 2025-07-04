from .base import *
# Development settings
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1','localhost']

DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR/ "static", "./static/",
]