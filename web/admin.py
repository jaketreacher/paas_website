from django.contrib import admin
from django.db.models import Count
from django.conf import settings
from django.utils.html import mark_safe

from .models import Event, EventDateTime


class EventDateTimeInline(admin.TabularInline):
    model = EventDateTime


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        img = '<img src="{url}" style="width:75px">'
        if obj.thumbnail_img:
            img = img.format(url=obj.thumbnail_img.url)
        else:
            img = img.format(url='https://via.placeholder.com/225x400')

        return mark_safe(img)

    list_display = ['name', 'slug', 'open_date', 'event_range', 'thumbnail']
    list_filter = ['open_date']
    search_fields = ['name']
    ordering = ['open_date']
    inlines = [EventDateTimeInline]
