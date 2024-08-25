from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import Group

import logging

logger = logging.getLogger("authentication")

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    # logger.debug("----CUSTOM ADAPTER CALLED----")
    def save_user(self, request, sociallogin, form=None):
        # logger.debug("----CUSTOM SAVE_USER CALLED----")
        # logger.debug(f"Social login data: {sociallogin.account.extra_data}")
        # Standard save process
        user = super().save_user(request, sociallogin, form)

        # Extract Keycloak roles. This part needs to be adapted based on how the roles are received.
        # For example, assuming roles are in `sociallogin.account.extra_data['roles']`
    #     keycloak_roles = sociallogin.account.extra_data.get('roles', [])

    #     # Process Keycloak roles
    #     self.process_keycloak_roles(user, keycloak_roles)

    #     return user

    # def process_keycloak_roles(self, user, roles):
    #     # Here, implement the logic to map Keycloak roles to Django groups
    #     # This is a basic implementation. Adjust it according to your needs.
    #     for role_name in roles:
    #         group, _ = Group.objects.get_or_create(name=role_name)
    #         user.groups.add(group)

provider_classes = []
