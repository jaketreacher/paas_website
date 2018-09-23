from django.conf import settings
from django.shortcuts import render


def home(request):
    return render(request, "web/pages/home.html")


def about(request):
    return render(request, "web/pages/about.html")


def memberships(request):
    # Temporarily grab link from .env
    params = {
        "form_link": settings.MEMBER_FORM_LINK
    }
    return render(request, "web/pages/memberships.html", params)


def friends(request):
    params = {
        "form_link": settings.FRIEND_FORM_LINK
    }
    return render(request, "web/pages/friends.html", params)


def contact(request):
    params = {
        "email": settings.CONTACT_EMAIL,
        "facebook": settings.CONTACT_FACEBOOK,
        "instagram": settings.CONTACT_INSTAGRAM,
        "abn": settings.CONTACT_ABN
    }
    return render(request, "web/pages/contact.html", params)
