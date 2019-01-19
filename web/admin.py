from django.contrib import admin
from django.db.models import Count
from django.conf import settings

from .models import Event, EventDateTime


class EventDateTimeInline(admin.TabularInline):
    model = EventDateTime


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'open_date', 'event_range']
    list_filter = ['open_date']
    search_fields = ['name']
    ordering = ['open_date']
    inlines = [EventDateTimeInline]
