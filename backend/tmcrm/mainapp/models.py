from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

from .validators import color_regex
from .fields import MonthDayField
from .managers import (
    OrgRestrictedManager,
    OrgFullAccessManager,
    OrgCreatorManager,
)
from django.db import models
from .exceptions.user_exceptions import UserHasNoOrg
from .constants import UserRole, TIMEZONE_CHOICES


class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_%(class)s_set",
    )

    objects = OrgFullAccessManager()
    org_objects = OrgRestrictedManager()
    create_manager = OrgCreatorManager()

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    def __str__(self):
        return self.name


class BaseModelOrg(models.Model):
    org = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_%(class)s_set",
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    objects = OrgFullAccessManager()
    org_objects = OrgRestrictedManager()
    create_manager= OrgCreatorManager()

    @property
    def get_org(self) -> Organization | None:
        """
        Возвращает организацию или None, если org отсутствует.
        """
        return self.org

    @property
    def has_org(self) -> bool:
        """Проверка наличия организации"""
        return self.org is not None

    class Meta:
        abstract = True

    def clean(self):
        errors = {}

        for field in self._meta.fields:

            if isinstance(field, (models.ForeignKey, models.OneToOneField)):
                related_obj = getattr(self, field.name, None)

                if related_obj and hasattr(related_obj, "org"):

                    related_org = getattr(related_obj, "org", None)
                    if related_org is not None and related_org != self.org:
                        errors[field.name] = (
                            f"Поле '{field.name}' ссылается на объект с другой организации: "
                            f" (ожидалось: {self.org} получено: {related_org})"
                        )
        if errors:
            raise ValidationError(errors)


class SubjectColor(BaseModelOrg):
    title = models.CharField(max_length=30, null=True)
    color_hex = models.CharField(max_length=7, validators=[color_regex])

    class Meta:
        verbose_name = "Цвет предмета"
        verbose_name_plural = "Цвета предметов"

    def __str__(self):
        return f"{self.title}"


class User(AbstractUser, BaseModelOrg):
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.USER)

    def has_role(self, *roles) -> bool:
        return getattr(self, "role", None) in roles

    def __str__(self):
        return f"{self.username} ({self.role})"


    def get_student_profile(self):
        return getattr(self, "student_profile", None)

    def get_manager_profile(self):
        return getattr(self, "manager_profile", None)

    def get_teacher_profile(self):
        return getattr(self, "teacher_profile", None)


class UserSettings(BaseModelOrg):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")

    def __str__(self):
        return f"Настройки пользователя {self.user.username}"

    class Meta:
        verbose_name = "Настройки пользователя"
        verbose_name_plural = "Настройки пользователя"


class OrgSettings(BaseModelOrg):
    org = models.OneToOneField(
        Organization, on_delete=models.CASCADE, related_name="settings"
    )

    timezone = models.CharField(
        max_length=32,
        choices=TIMEZONE_CHOICES,
        default="UTC",
        help_text="Часовой пояс организации",
    )
    repeat_lessons_until = MonthDayField(
        default="08-31"
    )

    class Meta:
        verbose_name = "Настройки организации"
        verbose_name_plural = "Настройки организации"

    def __str__(self):
        return f"Настройки {self.org.name}"


class ManagerProfile(BaseModelOrg):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="manager_profile", null=True)
    employer = models.OneToOneField("employers.Employer", on_delete=models.CASCADE, related_name="profile")      

class TeacherProfile(BaseModelOrg):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher_profile", null=True)
    teacher = models.OneToOneField("employers.Teacher", on_delete=models.CASCADE, related_name="profile")      


class StudentProfile(BaseModelOrg): 
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student_profile", null=True
    )
    student = models.OneToOneField("students.Student", on_delete=models.CASCADE, related_name="profile")
