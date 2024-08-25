from django.shortcuts import render
from user_authentication.decorators import keycloak_role_required


# Create your views here.
def landing_page(request):
    # from django.contrib.sessions.models import Session
    # all_sessions = Session.objects.all()
    # logger.warning("REMOVING All Sessions:")

    # for session in all_sessions:
    #     logger.warning(session.get_decoded())
    #     session.delete()
    return render(request, "landing_page.html")

def impressum(request):
    return render(request, "about/impressum.html")

def about_us(request):
    return render(request, "about/about_us.html")

def privacy(request):
    return render(request, "about/privacy.html")

@keycloak_role_required('coloreg-user')
def coloreg_instructions_summary(request):
    return render(request, "coloreg/instructions/summary.html")

@keycloak_role_required('coloreg-user')
def coloreg_security_concept(request):
    return render(request, "coloreg/security/concept.html")

@keycloak_role_required('coloreg-user')
def coloreg_security_study_hdd(request):
    return render(request, "coloreg/security/study-hdd.html")
