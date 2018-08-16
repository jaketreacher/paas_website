from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("memberships", views.memberships, name="memberships"),
    path("contact", views.contact, name="contact"),
    path("balltampering", views.balltampering, name="balltampering")
]

if not settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
