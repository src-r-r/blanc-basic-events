from django.contrib import admin
from .models import Event, RecurringEvent, RecurringEventExclusion


class RecurringEventInline(admin.TabularInline):
    model = RecurringEvent
    extra = 1


class RecurringEventExclusionInline(admin.TabularInline):
    model = RecurringEventExclusion
    extra = 1


class EventAdmin(admin.ModelAdmin):
    inlines = [
        RecurringEventInline,
    ]


admin.site.register(Event, EventAdmin)
