# content_manatement/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("about/impressum/", views.impressum, name="impressum"),
    path("about/about-us/", views.about_us, name="about_us"),
    path("about/privacy/", views.privacy, name="privacy"),

    # ColoReg
    ## Study Information
    path("coloreg/instructions/summary/", views.coloreg_instructions_summary, name="coloreg_instructions_summary"),

    ## IT Security
    path("coloreg/security/concept/", views.coloreg_security_concept, name="coloreg_security_concept"),
    path("coloreg/security/study-hdd/", views.coloreg_security_study_hdd, name="coloreg_security_study-hdd"),
]


