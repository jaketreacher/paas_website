from django.db import models
from django.db.models import Case, Max, Value, When
from django.utils import timezone
from preferences.models import Preferences

from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from collections import namedtuple


class EventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .annotate(last_show=Max('eventdatetime__datetime')) \
            .annotate(status=Case(
                When(open_date__gte=timezone.now(), then=Value(Event.STATE.HIDDEN)),
                When(last_show__lt=timezone.now(), then='end_action'),
                default=Value(Event.STATE.ACTIVE),
                output_field=models.CharField(max_length=1)
            ))


class Location(models.Model):
    name = models.CharField(max_length=128)
    details = models.TextField(blank=True, null=True)
    map_url = models.URLField(
        max_length=512,
        help_text='Enter the `src` component of an embedded map.',
        blank=True, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Event \'{}\' ({})'.format(self, self.pk)


class Event(models.Model):
    name = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=128, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True)
    slug = models.SlugField(max_length=32, unique=True)
    booking_url = models.URLField(help_text='ex. TryBooking URL', blank=True, null=True)
    open_date = models.DateTimeField(help_text='The date/time which the event will become visible.')

    thumbnail_img = FilerImageField(
        blank=True, null=True,
        related_name='thumbnail_img_event',
        on_delete=models.SET_NULL,
        help_text='The image that will display in the list of events.')
    hero_img = FilerImageField(
        blank=True, null=True,
        related_name='hero_img_event',
        on_delete=models.SET_NULL,
        help_text='The header image that will display on the event page.')
    description = models.TextField(blank=True, null=True)

    objects = EventManager()

    STATE = namedtuple('STATE', ['ACTIVE', 'ARCHIVED', 'HIDDEN'])('A', 'R', 'H')

    END_ACTION_CHOICES = (
        (STATE.ARCHIVED, 'Archive'),
        (STATE.HIDDEN, 'Hide'),
    )

    end_action = models.CharField(
        max_length=1,
        choices=END_ACTION_CHOICES,
        default=STATE.ARCHIVED,
        help_text='The action to take after the final event date has passed. '
                  'Archived events will display under \'Past Events\'. Hidden events will not be shown.'
    )

    def event_range(self):
        query_set = self.eventdatetime_set

        formatted_string = ''

        if query_set.count() > 1:  # Range
            start = query_set.first().datetime.strftime(EventDateTime.FORMAT_STRING_SHORT)
            end = query_set.last().datetime.strftime(EventDateTime.FORMAT_STRING_SHORT)
            formatted_string = '{} - {}'.format(start, end)
        elif query_set.count() == 1:  # Single
            single = query_set.first().datetime.strftime(EventDateTime.FORMAT_STRING_SHORT)
            formatted_string = str(single)
        else:  # None
            formatted_string = '- No Dates -'

        return formatted_string
    event_range.short_description = 'Event Range'

    class Meta:
        ordering = ('open_date',)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Event \'{}\' ({})'.format(self, self.pk)


class EventDateTime(models.Model):
    FORMAT_STRING = '%a, %d %b %Y'  # example: `Mon, 01 Jan 1990`
    FORMAT_STRING_SHORT = '%d.%m.%y'  # example: `01.01.90`
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    datetime = models.DateTimeField()

    class Meta:
        ordering = ('datetime',)

    def __str__(self):
        return self.datetime.strftime(self.FORMAT_STRING)

    def __repr__(self):
        return '<EventDateTime: \'{}\', {} ({})'.format(self, self.event, self.pk)


class SitePreferences(Preferences):
    class Meta:
        verbose_name = 'Preferences'
        verbose_name_plural = 'Preferences'

    home_title = models.TextField(blank=True, null=True)

    for section in ['about', 'membership', 'friend', 'contact']:
        locals()['{}_title'.format(section)] = models.CharField(max_length=50, blank=True, null=True)
        locals()['{}_text'.format(section)] = models.TextField(blank=True, null=True)

    member_form = models.URLField(
        help_text='The link for the member signup form.',
        blank=True, null=True)
    friend_form = models.URLField(
        help_text='The link for the friend signup form.',
        blank=True, null=True)

    email = models.EmailField(blank=True, null=True)
    facebook = models.CharField(
        max_length=50,
        help_text='Facebook username',
        blank=True, null=True)
    instagram = models.CharField(
        max_length=50,
        help_text='Instagram username',
        blank=True, null=True)
    abn = models.CharField(
        verbose_name='ABN',
        help_text='Australian Business Number. Include space formatting as desried.',
        max_length=20, blank=True, null=True)

    def __str__(self):
        return 'Site Preferences'
