import pytz
from typing import Literal
from django.db import models

HttpMethodLiteral = Literal["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]


class UserRole(models.TextChoices):
    ADMIN = "admin", "Администратор"
    MANAGER = "manager", "Менеджер"
    USER = "user", "Пользователь"


TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.all_timezones]
