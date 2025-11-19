from django.contrib import admin
from .models import *
from django.apps import apps
from mainapp.admin import BaseAdminFilterView
from django.contrib.admin.sites import AlreadyRegistered
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule


app_models = apps.get_app_config('lesson_schedule').get_models()


class ScheduleAdmin(BaseAdminFilterView):
    readonly_fields = ('week_day', )
    list_display = ('teacher', 'start_time', 'end_time', 'date', 'classroom', 'is_completed')
    list_filter = ('teacher__employer', 'start_time', 'end_time', 'date')
admin.site.register(Lesson, ScheduleAdmin)

class PeriodScheduleAdmin(BaseAdminFilterView):
    list_display = ('title', 'period')
admin.site.register(PeriodLesson, PeriodScheduleAdmin)


class AttendanceAdmin(BaseAdminFilterView):
    list_display = ("student", "lesson_date", "was_present")
admin.site.register(Attendance, AttendanceAdmin)


for model in app_models:
    try:
        if issubclass(model, BaseModelOrg):
            admin.site.register(model, BaseAdminFilterView)

        else: admin.site.register(model)

    except AlreadyRegistered:
        ...