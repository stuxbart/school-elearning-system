from django.contrib import admin

from .models import Calendar, Event, Participation, CalendarShareToken
# Register your models here.
admin.site.register(Calendar)
admin.site.register(Event)
admin.site.register(Participation)
admin.site.register(CalendarShareToken)