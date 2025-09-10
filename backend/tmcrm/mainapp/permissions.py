import logging
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from mainapp.models import BaseModelOrg
from django.shortcuts import get_object_or_404
from django.db import models


logger = logging.getLogger(__name__)

class IsSameOrganization(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: BaseModelOrg):

        if request.user.is_superuser:
            return True

        if hasattr(obj, "org"):
            return obj.org == request.user.org
        else:
            raise PermissionDenied(
                "Объект не имеет 'org', проверка организации невозможна. "
                "Пермишн применен к модели не имющей org"
            )

class OrgNameMatchPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj == request.user.org



class OrgParamsPermission(permissions.BasePermission):
    """
    Проверяет для указанных query-параметров,
    что объекты с этими id принадлежат организации пользователя.
    """

    def __init__(self, param_model_map: dict[str, type[models.Model]]):
        self.param_model_map = param_model_map
        self.message = "Недоступные параметры"


    def has_permission(self, request, view) -> bool:
        if request.user.is_superuser:
            return True

        for param, model in self.param_model_map.items():
            param_id = request.query_params.get(param)
            if param_id is not None:
                obj = get_object_or_404(model, id=param_id)
                if getattr(obj, "org_id", None) != getattr(
                    request.user, "org_id", None
                ):
                    return False
        return True
    





