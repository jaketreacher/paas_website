from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()


@register.simple_tag(takes_context=True)
def selected(context, name):
    path = context['request'].path
    url = reverse(name)

    if path == url:
        return "selected"
