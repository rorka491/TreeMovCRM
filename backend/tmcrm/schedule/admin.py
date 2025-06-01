from django.contrib import admin
from .models import *
from django.apps import apps
from mainapp.admin import BaseAdminFilterView
from django.contrib.admin.sites import AlreadyRegistered

app_models = apps.get_app_config('schedule').get_models()


class ScheduleAdmin(BaseAdminFilterView):
    readonly_fields = ('week_day', )
    list_display = ('teacher', 'lesson', 'start_time', 'end_time', 'date')
    list_filter = ('teacher__employer', 'lesson', 'start_time', 'end_time', 'date')
admin.site.register(Schedule, ScheduleAdmin)





for model in app_models:
    try:
        if issubclass(model, BaseModelOrg):
            admin.site.register(model, BaseAdminFilterView)

        else: admin.site.register(model)

    except AlreadyRegistered:
        ...







