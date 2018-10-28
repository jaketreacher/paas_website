from django.conf import settings
from django.db.models import Max, Q
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from .models import Event


def home(request):
    return render(request, 'web/pages/home.html')


def about(request):
    return render(request, 'web/pages/about.html')


def memberships(request):
    # Temporarily grab link from .env
    params = {
        'form_link': settings.MEMBER_FORM_LINK
    }
    return render(request, 'web/pages/memberships.html', params)


def friends(request):
    params = {
        'form_link': settings.FRIEND_FORM_LINK
    }
    return render(request, 'web/pages/friends.html', params)


def contact(request):
    params = {
        'email': settings.CONTACT_EMAIL,
        'facebook': settings.CONTACT_FACEBOOK,
        'instagram': settings.CONTACT_INSTAGRAM,
        'abn': settings.CONTACT_ABN
    }
    return render(request, 'web/pages/contact.html', params)


def event_list_view(request):
    params = {
        'current_events': Event.objects.filter(status=Event.STATE.ACTIVE),
        'expired_events': Event.objects.filter(status=Event.STATE.ARCHIVED)
    }
    return render(request, 'web/pages/event-list.html', params)


def event_view(request, slug):
    # TODO: Expired events use a different template which displays a photo gallery
    event = get_object_or_404(Event, slug=slug)

    if event.status != Event.STATE.ACTIVE:
        return redirect('home')

    params = {
        'event': event
    }
    return render(request, 'web/pages/event.html', params)
