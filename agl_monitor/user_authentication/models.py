from django.contrib.auth.models import User, Group
from django.db import models
from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.db import transaction

from allauth.socialaccount.signals import pre_social_login

import logging

logger = logging.getLogger("authentication")

@receiver(pre_social_login)
def handle_keycloak_roles(sender, request, sociallogin, **kwargs):
    # Assuming the roles are in sociallogin.account.extra_data['roles']
    # logger.debug("----PRE SOCIAL LOGIN CALLED----")
    # logger.debug(f"Social login data: {sociallogin.account.extra_data}")
    keycloak_groups = sociallogin.account.extra_data.get('groups', [])
    
    user = sociallogin.user

    # check if user is already in the database by username
    # if already available, we need to assign the correct id to the user object

    if not user.id:
        with transaction.atomic():
            # check for existing user:
            existing_user = User.objects.filter(username=user.username).first()
            
            if existing_user:
                user.id = existing_user.id

            # Set a basic field to trigger save
            logger = logging.getLogger("authentication")
            logger.debug(f"Creating user {user.username}")
            user.save()  # This ensures the user has an ID for many-to-many relationships

            logger.debug(f"Saved user {user.username} with id {user.id}")
            logger.debug(f"sociallogin.account.extra_data: {sociallogin.account.extra_data.get('groups', [])}")

    # Assign new roles from Keycloak
    for role_name in keycloak_groups:
        group, _ = Group.objects.get_or_create(name=role_name)
        user.groups.add(group)

    if 'admin' in keycloak_groups:
        user.is_staff = True
        user.is_superuser = True
        user.save()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    keycloak_roles = models.TextField()

    def __str__(self):
        return self.user.username
