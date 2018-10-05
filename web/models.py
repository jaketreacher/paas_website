from django.db import models
from django.utils import timezone


class Event(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField()
    url = models.URLField(help_text="The location of the booking site.")
    open_date = models.DateTimeField(help_text="The date/time which the event will become visible.")

    END_ACTION_CHOICES = (
        ('A', 'Archive'),
        ('H', 'Hide'),
    )
    end_action = models.CharField(
        max_length=1,
        choices=END_ACTION_CHOICES,
        default=END_ACTION_CHOICES[0][0],
        help_text="The action to take after the final event date has passed. "
                  "Archived events will display under 'Past Events'. Hidden events will not be shown."
    )

    def event_range(self):
        query_set = self.eventdatetime_set

        formatted_string = ""

        if query_set.count() > 1:  # Range
            start = query_set.first().datetime.strftime(EventDateTime.FORMAT_STRING_SHORT)
            end = query_set.last().datetime.strftime(EventDateTime.FORMAT_STRING_SHORT)
            formatted_string = f"{start} – {end}"
        elif query_set.count() == 1:  # Single
            single = query_set.first().datetime.strftime(EventDateTime.FORMAT_STRING_SHORT)
            formatted_string = f"{single}"
        else:  # None
            formatted_string = "- No Dates -"

        return formatted_string
    event_range.short_description = 'Event Range'

    class Meta:
        ordering = ('open_date',)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Event: '{self}' ({self.pk})>"


class EventDateTime(models.Model):
    FORMAT_STRING = '%a, %d %b %Y @ %I:%M%p'  # example: `Mon, 01 Jan 1990 @ 12:01PM`
    FORMAT_STRING_SHORT = '%a, %d %b %Y'  # example: `Mon, 01 Jan 1990`
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    datetime = models.DateTimeField()

    class Meta:
        ordering = ('datetime',)

    def __str__(self):
        return self.datetime.strftime(self.FORMAT_STRING)

    def __repr__(self):
        return f"<EventDateTime: '{self}', {self.event} ({self.pk})>"


class EventPage(models.Model):
    background = models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d/')
    mobile = models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d/')
    tablet = models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d/')
    desktop = models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d/')

    event = models.OneToOneField(Event, on_delete=models.CASCADE)
