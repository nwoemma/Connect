from .base import *
import os
import dj_database_url

DEBUG = True
ALLOWED_HOSTS = ["www.egapp.com","127.0.0.1", "ewapp.com","connect-d9z6.onrender.com",]

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'Connect/staticfiles')
