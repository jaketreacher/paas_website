from django import template
from django.conf import settings
from django.urls import reverse, NoReverseMatch
from django.templatetags.static import StaticNode

from os import path

register = template.Library()


@register.simple_tag(takes_context=True)
def selected(context, name):
    path = context['request'].path
    url = reverse(name)

    if path == url:
        return 'nav-menu__item--selected'


@register.simple_tag(takes_context=True)
def media(context, path):
    return path.join(settings.MEDIA_URL, path)


@register.simple_tag(takes_context=True)
def absolute_uri(context, url, resource_type=None):
    request = context['request']
    if resource_type == 'static':
        url = StaticNode.handle_simple(url)
    return request.build_absolute_uri(url)
