from django.contrib import admin
from .models import *
from django.apps import apps


app_models = apps.get_app_config('schedule').get_models()

class ScheduleAdmin(admin.ModelAdmin):
    readonly_fields = ('week_day',)

admin.site.register(Schedule, ScheduleAdmin)

for model in app_models:
    if model != Schedule:
        admin.site.register(model)






