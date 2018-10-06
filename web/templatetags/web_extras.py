from django import template
from django.conf import settings
from django.urls import reverse, NoReverseMatch

from os import path

register = template.Library()


@register.simple_tag(takes_context=True)
def selected(context, name):
    path = context['request'].path
    url = reverse(name)

    if path == url:
        return "selected"


@register.simple_tag(takes_context=True)
def media(context, path):
    return path.join(settings.MEDIA_URL, path)
