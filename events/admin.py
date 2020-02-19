from django.contrib import admin
from .models import Events

class EventAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_type', 'event_name','event_location','event_date','event_time','event_time_type','event_time_zone','event_description')
admin.site.register(Events, EventAdmin)