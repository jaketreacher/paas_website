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
    return render(request, 'web/pages/memberships.html')


def friends(request):
    return render(request, 'web/pages/friends.html')


def contact(request):
    return render(request, 'web/pages/contact.html')


def event_list_view(request):
    # staff can see hidden pre-released events (but not hidden expired)
    if request.user.is_staff or request.user.is_superuser:
        prerelease = Event.objects.filter(status=Event.STATE.HIDDEN).filter(open_date__gte=timezone.now())
        # ce_qs = current event query set
        ce_qs = Event.objects.filter(
            Q(status=Event.STATE.ACTIVE) |
            Q(
                Q(status=Event.STATE.HIDDEN) &
                Q(open_date__gte=timezone.now())
            )
        )
    else:
        ce_qs = Event.objects.filter(status=Event.STATE.ACTIVE)

    params = {
        'current_events': ce_qs,
        'expired_events': Event.objects.filter(status=Event.STATE.ARCHIVED)
    }

    return render(request, 'web/pages/event-list.html', params)


def event_view(request, slug):
    # TODO: Expired events use a different template which displays a photo gallery
    event = get_object_or_404(Event, slug=slug)

    if not (request.user.is_staff or request.user.is_superuser):
        if event.status != Event.STATE.ACTIVE:
            return redirect('home')

    params = {
        'event': event
    }
    return render(request, 'web/pages/event.html', params)
