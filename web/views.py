from django.conf import settings
from django.shortcuts import render


def home(request):
    return render(request, "web/pages/home.html")


def about(request):
    return render(request, "web/pages/about.html")


def memberships(request):
    # Temporarily grab link from .env
    params = {
        "form_link": settings.FORM_LINK
    }
    return render(request, "web/pages/memberships.html", params)


def contact(request):
    params = {
        "email": settings.CONTACT_EMAIL,
        "facebook": settings.CONTACT_FACEBOOK,
        "instagram": settings.CONTACT_INSTAGRAM,
        "abn": settings.CONTACT_ABN
    }
    return render(request, "web/pages/contact.html", params)


def balltampering(request):
    return render(request, "web/pages/balltampering.html")
