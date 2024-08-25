import os
import json
from .django_settings import *
from ..base_urls import KEYCLOAK_BASE_URL, KEYCLOAK_REALM_BASE_URL, HOME_URL

# Get environment variables
CLIENT_ID = os.environ.get('KEYCLOAK_CLIENT', 'test_client')
CLIENT_SECRET = os.environ.get('KEYCLOAK_SECRET', 'such-secrecy-wooooow') #TODO make


AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
]

USERSESSIONS_TRACK_ACTIVITY = True # Requires allauth.usersessions.middleware.UserSessionsMiddleware
USERSESSIONS_ADAPTER = "allauth.usersessions.adapter.DefaultUserSessionsAdapter" # is default

SOCIALACCOUNT_ADAPTER = 'user_authentication.adapters.CustomSocialAccountAdapter'

SOCIALACCOUNT_PROVIDERS = {
    "openid_connect": {
        "APPS": [
            {
                "provider_id": "keycloak",
                "name": "Keycloak",
                "client_id": CLIENT_ID,
                "secret": CLIENT_SECRET,
                "settings": {
                    "server_url": f"{KEYCLOAK_BASE_URL}/realms/master/.well-known/openid-configuration",
                },
            }
        ]
    }
}


LOGIN_REDIRECT_URL = "landing_page"
LOGOUT_REDIRECT_URL = "landing_page"

