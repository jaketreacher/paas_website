from django.db import models
from django.db.models import Case, F, Max, Q, Value, When
from django.template import loader, Context
from django.utils import timezone

import os
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


class Event(models.Model):
    name = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=128, blank=True, null=True)
    location = models.CharField(max_length=128, blank=True, null=True)
    slug = models.SlugField(max_length=32, unique=True)
    booking_url = models.URLField(help_text='ex. TryBooking URL', blank=True, null=True)
    open_date = models.DateTimeField(help_text='The date/time which the event will become visible.')

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

    @property
    def get_preview_url(self):
        """
        Get the URL of the image that will be displayed on
        the event-list page. Ideally, this will be the
        thumbnail.
        """
        sizes = ['thumbnail', 'mobile', 'tablet', 'desktop']

        for size in sizes:
            image = getattr(self.eventpage, size)
            if image:
                return image.url

        return None

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


class EventPage(models.Model):
    background = models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d/')
    thumbnail = models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d/')
    mobile = models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d/')
    tablet = models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d/')
    desktop = models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d/')
    css = models.TextField(blank=True, null=True)
    event = models.OneToOneField(Event, on_delete=models.CASCADE)

    def _build_css(self):
        template = loader.get_template('web/pages/event.css.html')
        style = ' '.join(template.render({'eventpage': self}).split())  # join/split used to remove excessive whitespace
        type(self).objects.filter(id=self.id).update(css=style)

    def _clean_images(self, old_self):
        for field in old_self._meta.get_fields():
            if isinstance(field, models.ImageField):
                old_image = getattr(old_self, field.name)
                new_image = getattr(self, field.name)
                # if the field existed before and it has changed
                if old_image and old_image != new_image:
                    # remove the previous file
                    try:
                        os.remove(old_image.path)
                    except FileNotFoundError:
                        pass

    def save(self, *args, **kwargs):
        try:
            old_self = EventPage.objects.get(pk=self.pk)
        except EventPage.DoesNotExist:
            old_self = None
        super(EventPage, self).save(*args, **kwargs)
        if old_self:
            self._clean_images(old_self)
        self._build_css()
