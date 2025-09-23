from typing import Any, TypeVar, Generic, TYPE_CHECKING, Type, Optional
from django.db import models
from django.db.models import QuerySet, Q, Model
from .middleware.threadlocals import get_current_user, get_current_org
from django.contrib.auth import get_user_model
from .exceptions.user_exceptions import UserNotHasBeenGet

if TYPE_CHECKING:
    from mainapp.models import User, Organization

T = TypeVar("T", bound=models.Model)

class OrgQuerySet(QuerySet):

    def filter_by_org(self, org):
        return self.filter(Q(org=org) | Q(org__isnull=True))

    def filter_by_user(self, user: "User") -> QuerySet:
        if user.has_role("admin"):
            return self

        if user.has_org:
            user_org = user.get_org
            return self.filter_by_org(user_org)

        return self.filter(org__isnull=True)

    def filter_by_current_user(self):
        """
        Возвращает записи по организации текущего пользователя.
        """
        current_user = get_current_user()
        if current_user:
            return self.filter_by_user(user=current_user)
        raise UserNotHasBeenGet()


class OrgRestrictedManager(models.Manager):
    def get_queryset(self):
        return OrgQuerySet(self.model, using=self._db).filter_by_current_user()



class OrgFullAccessManager(models.Manager):
    def get_queryset(self):
        return OrgQuerySet(self.model, using=self._db)

    def filter_by_org(self, org):
        return self.get_queryset().filter_by_org(org)

    def filter_by_user(self, user):
        return self.get_queryset().filter_by_user(user)


class OrgCreator(QuerySet):

    def create_with_user(self, user: "User", with_org: bool, **kwargs):
        """Если with_org True тогда будет создан экземпляр
        с организацией если нет тогда будет создан
        обычный объект с полем create_by"""
        if not user:
            user = get_current_user()

        model_cls = self.model
        user_org = user.get_org()
        if with_org and user_org is not None:
            return model_cls.objects.create(org=user_org, created_by=user, **kwargs)

        return model_cls.objects.create(created_by=user, **kwargs)


class OrgCreatorManager(models.Manager[T]):

    def get_queryset(self) -> QuerySet[T]:
        return OrgQuerySet(self.model, using=self._db)

    def create(
        self,
        org: "Optional[Organization]" = None,
        created_by: "Optional[User]" = None,
        **kwargs: Any
    ) -> Any:
        
        org = org or get_current_org()
        created_by = created_by or get_current_user()

        if org is None:
            raise ValueError("Организация не определена и не передана явно")
        if created_by is None:
            raise ValueError("Пользователь не определён и не передан явно")

        kwargs["org"] = org
        kwargs["created_by"] = created_by

        return super().create(**kwargs)
