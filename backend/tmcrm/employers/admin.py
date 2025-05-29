from django.contrib import admin
from .models import *
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from mainapp.admin import BaseAdminFilterView


app_models = apps.get_app_config('employers').get_models()



for model in app_models:
    try:
        if issubclass(model, BaseModelOrg):
            admin.site.register(model, BaseAdminFilterView)
        else:
            admin.site.register(model)
    except AlreadyRegistered:
        ...
