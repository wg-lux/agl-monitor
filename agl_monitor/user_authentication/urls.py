# urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('user-status/', views.user_status, name='user_status'),
    path('test-auth-view/', views.test_auth_view, name='test_auth_view'),
    path("redirect-after-logout/", views.redirect_after_logout, name="redirect_after_logout"),
]
