from .base import *
import os
import dj_database_url

ALLOWED_HOSTS = ["www.ewapp.com", "ewapp.com",]

DATABASE = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'Connect/staticfiles')