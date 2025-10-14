from django.contrib import admin
from .models import *
from django.apps import apps

app_models = apps.get_app_config('financial_reporting').get_models()

for model in app_models:
    admin.site.register(model)
