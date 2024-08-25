from ..settings_base import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'default_secret_key')
print(f"CHECK SECRET KEYYYY: {SECRET_KEY}")

DEBUG = False

ALLOWED_HOSTS = [
    "127.0.0.1",
    "agl-monitor-intern.endo-reg.net",
    # "*.endo-reg.net",
    "172.16.255.4"
]

SECURE_SSL_REDIRECT = True
OIDC_VERIFY_SSL = True

# Production database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'prod_db_name',
#         'USER': 'prod_db_user',
#         'PASSWORD': 'prod_db_password',
#         'HOST': 'prod_db_host',
#         'PORT': 'prod_db_port',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


