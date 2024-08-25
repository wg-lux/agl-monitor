from ..settings_base import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'your_dev_secret_key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECRET_KEY = "django-insecure-powk20*'__!xpq@"
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# TODO MIGRATE TO PRODUCTION
# settings_prod.py
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True