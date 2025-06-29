from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from .validators import color_regex
from .fields import MonthDayField
from django.conf import settings
import pytz

class CreatedBy(models.Model):
    create_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_%(class)s_set'
    )

    class Meta:
        abstract = True

class Organization(CreatedBy):
    name = models.CharField(max_length=100, unique=True)

    
    class Meta:
        verbose_name = 'Организация' 
        verbose_name_plural = 'Организации' 

    def __str__(self):
        return self.name




class BaseModelOrg(models.Model): 
    org = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='%(class)s'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_%(class)s_set'
    )
    
    class Meta:
        abstract = True


    def clean(self):
        errors = {}

        for field in self._meta.fields:

            if isinstance(field, (models.ForeignKey, models.OneToOneField)):
                related_obj = getattr(self, field.name, None)
                
                if related_obj and hasattr(related_obj, 'org'):
                    
                    related_org = getattr(related_obj, 'org', None)
                    if related_org is not None and related_org != self.org:
                        errors[field.name] = (
                            f"Поле '{field.name}' ссылается на объект с другой организации: "
                            f" (ожидалось: {self.org} получено: {related_org})"
                        )
        if errors:
            raise ValidationError({'field': ['ошибка']})
        

    @classmethod
    def create_with_user_org(cls, user, **kwargs):
        return cls.objects.create(org=user.org, created_by=user, **kwargs)
    
    @classmethod
    def create_with_create_by(cls, user, **kwargs):
        return cls.objects.create(created_by=user, **kwargs)


class SubjectColor(BaseModelOrg):
    title = models.CharField(max_length=30, null=True)
    color_hex = models.CharField(max_length=7, validators=[color_regex])

    class Meta:
        verbose_name = 'Цвет предмета'
        verbose_name_plural = 'Цвета предметов'

    def __str__(self):
        return f'{self.title}'
    


class User(AbstractUser, BaseModelOrg):
    ROLES = (
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
        ('user', 'Пользователь'),
    )
    
    role = models.CharField(max_length=20, choices=ROLES, default='user')

    
    def __str__(self):
        return f"{self.username} ({self.role})"
    


class UserSettings(BaseModelOrg):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    repeat_lessons_until = MonthDayField(default='08-31') # Кастомное поле в формате MM-DD

    def __str__(self):
        return f'Настройки пользователя {self.user.username}'
    
    class Meta:
        verbose_name = 'Настройки пользоователя'
        verbose_name_plural = 'Настройки пользоователя'


class OrgSettings(BaseModelOrg):
    TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.all_timezones]

    timezone = models.CharField(
        max_length=32,
        choices=TIMEZONE_CHOICES,
        default='UTC',
        help_text='Часовой пояс организации'
    )
    


    class Meta:
        verbose_name = 'Настройки организации'
        verbose_name_plural = 'Настройки организации'

    def __str__(self):
        return f'Настройки {self.org.name}'






