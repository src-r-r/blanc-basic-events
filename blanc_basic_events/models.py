from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class AbstractSpecialEvent(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ForeignKey('assets.Image', null=True, blank=True)
    summary = models.CharField(max_length=100,
                               help_text='A short sentence description of the event')
    description = models.TextField(help_text='All of the event details we have')
    start = models.DateTimeField(help_text='Start time/date.')
    start_date = models.DateField(editable=False, db_index=True)
    final_date = models.DateField(blank=True, db_index=True,
                                  help_text='Last date this event appears on the list page')
    published = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ('start',)
        abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Used for easy queryset filtering
        self.start_date = self.start.date()

        # Set a default final date if one isn't given
        if not self.final_date:
            self.final_date = self.start.date()

        # If someone forgets to fix the final date after changing the event
        if self.final_date < self.start_date:
            self.final_date = self.start_date

        super(AbstractSpecialEvent, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('blanc_basic_events:specialevent-detail', (), {
            'slug': self.slug,
        })


class SpecialEvent(AbstractSpecialEvent):
    class Meta(AbstractSpecialEvent.Meta):
        swappable = 'EVENTS_SPECIAL_MODEL'


@python_2_unicode_compatible
class AbstractRecurringEvent(models.Model):
    DAY_CHOICES = (
        (7, 'Sunday'),  # We intentionally start on Sunday, but with isoweekday for numbering
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
    )

    title = models.CharField(max_length=100, db_index=True)
    image = models.ForeignKey('assets.Image', null=True, blank=True)
    description = models.TextField()
    day_of_the_week = models.PositiveSmallIntegerField(choices=DAY_CHOICES, db_index=True)
    frequency = models.CharField(default='Weekly', max_length=200)
    published = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ('day_of_the_week', 'title')
        abstract = True

    def __str__(self):
        return self.title


class RecurringEvent(AbstractRecurringEvent):
    class Meta(AbstractRecurringEvent.Meta):
        swappable = 'EVENTS_RECURRING_MODEL'