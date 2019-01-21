from django.contrib import admin
from django.contrib.sites.models import Site
from django.db.models import Count
from django.conf import settings
from django.utils.html import mark_safe
from preferences.admin import PreferencesAdmin

from .models import Event, EventDateTime, SitePreferences


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


@admin.register(SitePreferences)
class SitePreferencesAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    fieldsets = (
        ('Home', {
            'fields': ['home_title']
        }),
        ('About', {
            'fields': ['about_title', 'about_text']
        }),
        ('Membership', {
            'fields': ['membership_title', 'membership_text', 'member_form']
        }),
        ('Friend', {
            'fields': ['friend_title', 'friend_text', 'friend_form']
        }),
        ('Contact', {
            'fields': ['contact_title', 'contact_text', 'email', 'facebook', 'instagram', 'abn']
        }),
    )


admin.site.unregister(Site)
