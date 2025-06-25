from .base import *
import os
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ["www.ewapp.com", "ewapp.com","connect-d9z6.onrender.com",]

DATABASES = {
    'default': dj_database_url.config(
        default="postgresql://ewapp_user:nBXo6rooo5tchGzGSWiDzza5p35wDh7v@dpg-d1dhr7idbo4c73du05e0-a.frankfurt-postgres.render.com:5432/ewapp_db",
        conn_max_age=600,
        ssl_require=True
    )
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'Connect/staticfiles')
