from django.contrib import admin
from .models import *
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

class BaseAdminFilterView(admin.ModelAdmin):
    list_filter = ('org', )

    def get_list_display(self, request):
        base = super().get_list_display(request)
        return base + ('org',) if 'org' not in base else base


class UserAdmin(admin.ModelAdmin):
    list_filter = ('role', )
    list_display = ('username', 'role', 'is_superuser')
    list_editable = ('is_superuser', )
admin.site.register(User, UserAdmin)


app_models = apps.get_app_config('mainapp').get_models()




for model in app_models:
    try:
        if issubclass(model, BaseModelOrg):
            admin.site.register(model, BaseAdminFilterView)
        else:
            admin.site.register(model)

    except AlreadyRegistered:
        ...




