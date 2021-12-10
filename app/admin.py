from django.contrib import admin

from .models import Schedule

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'summary', 'description', 'start_time', 'end_time', 'room', 'date', 'created_at')

admin.site.register(Schedule, ScheduleAdmin)

# Register your models here.