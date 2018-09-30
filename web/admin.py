from django.contrib import admin

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
