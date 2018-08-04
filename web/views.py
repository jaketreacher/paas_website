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
