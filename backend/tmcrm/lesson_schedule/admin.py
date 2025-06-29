from django.contrib import admin
from .models import *
from django.apps import apps
from mainapp.admin import BaseAdminFilterView
from django.contrib.admin.sites import AlreadyRegistered
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule


app_models = apps.get_app_config('lesson_schedule').get_models()


class ScheduleAdmin(BaseAdminFilterView):
    readonly_fields = ('week_day', )
    list_display = ('teacher', 'lesson', 'start_time', 'end_time', 'date', 'is_completed')
    list_filter = ('teacher__employer', 'lesson', 'start_time', 'end_time', 'date')
admin.site.register(Schedule, ScheduleAdmin)

class PeriodScheduleAdmin(BaseAdminFilterView):
    list_display = ('title', 'period')
admin.site.register(PeriodSchedule, PeriodScheduleAdmin)





for model in app_models:
    try:
        if issubclass(model, BaseModelOrg):
            admin.site.register(model, BaseAdminFilterView)

        else: admin.site.register(model)

    except AlreadyRegistered:
        ...







