from django.contrib import admin
from django.db.models import Count
from django.conf import settings

from .models import Event, EventDateTime, EventPage


class EventDateTimeInline(admin.TabularInline):
    model = EventDateTime


class EventPageInline(admin.StackedInline):
    model = EventPage
    if settings.DEBUG:
        readonly_fields = ['css']
    else:
        exclude = ['css']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'open_date', 'event_range']
    list_filter = ['open_date']
    search_fields = ['name']
    ordering = ['open_date']
    inlines = [EventPageInline, EventDateTimeInline]
