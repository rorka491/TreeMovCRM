from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from mainapp.models import BaseModelOrg


class BaseAdminFilterView(admin.ModelAdmin):
    list_filter = ("org",)

    def get_list_display(self, request):
        base = super().get_list_display(request)
        return base + ("org",) if "org" not in base else base


app_models = apps.get_app_config("accounts").get_models()

for model in app_models:
    try:
        if issubclass(model, BaseModelOrg):
            admin.site.register(model, BaseAdminFilterView)
        else:
            admin.site.register(model)

    except AlreadyRegistered:
        ...
