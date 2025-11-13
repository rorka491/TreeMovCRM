from typing import Literal
import logging
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from mainapp.models import BaseModelOrg
from django.shortcuts import get_object_or_404
from django.db import models


logger = logging.getLogger(__name__)


class IsAuthenticatedAndSameOrganization(IsAuthenticated):
    """
    Проверяет, что пользователь авторизован.
    Если объект связан с организацией — требует совпадения org_id.
    Если объект не имеет org — доступен всем авторизованным пользователям.
    """

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        user = request.user

        if getattr(user, "is_superuser", False):
            return True

        if not getattr(user, "has_org", False):
            raise PermissionDenied("У пользователя нет организации")

        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if getattr(user, "is_superuser", False):
            return True

        obj_org = getattr(obj, "org_id", None)
        user_org = getattr(user, "org_id", None)

        if obj_org is None:
            return True

        return obj_org == user_org


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
