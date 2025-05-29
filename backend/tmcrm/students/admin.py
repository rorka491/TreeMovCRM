from django.contrib import admin
from .models import *
from django.apps import apps
from mainapp.admin import BaseAdminFilterView
from django.contrib.admin.sites import AlreadyRegistered


app_models = apps.get_app_config('students').get_models()

for model in app_models:
    try:
        if issubclass(model, BaseModelOrg):
            admin.site.register(model, BaseAdminFilterView)
        else:
            admin.site.register(model)
    except AlreadyRegistered:
        ...
