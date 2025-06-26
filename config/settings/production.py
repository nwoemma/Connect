from .base import *
import os
import dj_database_url

DEBUG = True
ALLOWED_HOSTS = ["www.ewapp.com","127.0.0.1", "ewapp.com","connect-d9z6.onrender.com",]

DATABASES = {
    'default': dj_database_url.config(
        default="postgresql://ewapp_user:KPSFZBsnL5Xrq8XquTcR1BQJ4zxFFbTo@dpg-d1e8as3e5dus73b50bgg-a.frankfurt-postgres.render.com:5432/ewapp_db_e9ed",
        conn_max_age=600,
        ssl_require=True
    )
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'Connect/staticfiles')
