from typing import TYPE_CHECKING, TypeVar
from functools import wraps
from django.core.cache import cache
from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.db.models import Q, QuerySet
from django.conf import settings
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.exceptions import NotAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.request import Request
from mainapp.serializers import BaseReadSerializer, BaseWriteSerializer
from .models import Organization
from .serializers import ColorSerializer, OrganizationWriteSerializer, OrganizationReadSerializer
from .permissions import IsSameOrganization, OrgNameMatchPermission
from .models import User, SubjectColor
from .middleware.threadlocals import get_current_user

if TYPE_CHECKING:
    from rest_framework import permissions
    from .serializers import (
        BaseReadSerializer,
        BaseWriteSerializer,
        BaseSerializerExcludeFields,
    )
    from rest_framework.serializers import BaseSerializer


T = TypeVar('T', bound=QuerySet)

class RequiredQueryParamsMixin:

    def _return_response_if_missing(self, missing: list):
        if missing:
            return Response(
                {p: ["This parameter is required."] for p in missing}, status=400
            )

    def validate_required_query_params(self, request, required_params):
        missing = [p for p in required_params if p not in request.GET]
        return self._return_response_if_missing(missing=missing)

    def validate_required_data(self, data, required_params):
        missing = [p for p in required_params if p not in data]
        return self._return_response_if_missing(missing=missing)

class GetCurrentSerializerMixin:
    read_serializer_class: type["BaseSerializer"] | None = None
    write_serializer_class: type["BaseSerializer"] | None = None
    serializer_class: type["BaseSerializer"] | None = None

    def get_serializer_class(
        self,
    ) -> type["BaseSerializer"]:
        """Метод возвращает нужный сериализатор в зависимости от метода"""
        if self.request.method in ("HEAD", "GET", "OPTIONS"):
            return self.read_serializer_class or self.serializer_class
        return self.write_serializer_class or self.serializer_class


class SelectRelatedViewSet(ModelViewSet):
    """
    Класс который будет использоваться для оптимизированных запросов
    и решения N+1 проблемы

    Наслдуется перед BaseViewSetWithOrdByOrg
    """

    select_related_fields = []
    prefetch_related_fields = []

    def get_queryset(self):
        qs = super().get_queryset()

        if self.select_related_fields:
            qs = qs.select_related(*self.select_related_fields)
        if self.prefetch_related_fields:
            qs = qs.prefetch_related(*self.prefetch_related_fields)

        return qs

class SelectrealtedByModelsViewSet(ModelViewSet):
    """
    То же самое решение только для вьюсетов которые используют несолько queryset'ов
    Класс который будет использоваться для оптимизированных запросов
    и решения N+1 проблемы

    Наслдуется перед BaseViewSetWithOrdByOrg
    Не наследуестя с SelectRelatedViewSet
    """

    select_related_fields_by_model: dict[str, tuple] = {}
    prefetch_related_fields_by_model: dict[str, tuple] = {}

    def optimize_queryset(self, queryset: T) -> T:
        model_name = queryset.model.__name__

        # select_related
        if self.select_related_fields_by_model:
            fields = self.select_related_fields_by_model.get(model_name, [])
            if fields:
                queryset = queryset.select_related(*fields)

        # prefetch_related
        if self.prefetch_related_fields_by_model:
            fields = self.prefetch_related_fields_by_model.get(model_name, [])
            if fields:
                queryset = queryset.prefetch_related(*fields)
        
        return queryset


class BaseViewAuthPermission(ModelViewSet):

    def get_permissions(self) -> list["permissions.BasePermission"]:
        return [IsAuthenticated(), IsSameOrganization()]


class BaseViewSetWithOrdByOrg(
    GetCurrentSerializerMixin, BaseViewAuthPermission
):
    """
    Базовый ViewSet с автоматической фильтрацией по организации пользователя
    и дополнительными проверками прав доступа
    """


    filter_backends = [DjangoFilterBackend]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["org"] = self.get_current_org(request.user).pk
        request._full_data = data
        return super().create(request, *args, **kwargs)

    def get_current_user(self) -> User:
        current_user = get_current_user()
        if isinstance(current_user, AnonymousUser):
            raise NotAuthenticated("Пользователь не аутентифицирован.")
        return current_user

    def get_current_org(self, user: User) -> Organization:
        org = user.get_org()
        if not org:
            raise ValueError("Организация не предоставлена")
        return org

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.get_current_user()
        return queryset.filter_by_user(user)



class OrganizationViewSet(
    GetCurrentSerializerMixin, BaseViewAuthPermission
):
    queryset = Organization.objects.all()
    read_serializer_class = OrganizationReadSerializer
    write_serializer_class = OrganizationWriteSerializer

    def get_permissions(self) -> list[BasePermission]:
        return [IsAuthenticated(), OrgNameMatchPermission()]


def base_search(func):
    @wraps(func)
    def wrapper(
        self: BaseViewSetWithOrdByOrg, request: Request, *args, **kwargs
    ) -> Response:
        query = request.data.get("query", "").strip()

        if not query:
            return Response({"error": "Пустой запрос"}, status=400)

        words = [word for word in query.split()]

        q: Q = func(self, request, words=words, *args, **kwargs)

        results = self.get_queryset().filter(q)
        serializer = self.serializer_class(results, many=True)
        return Response(serializer.data)

    return wrapper


class SubjectColorViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = SubjectColor.objects.all()
    serializer_class = ColorSerializer
