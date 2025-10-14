import pytz
from typing import Literal
from django.db import models

HttpMethodLiteral = Literal["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]


class NoteCategory(models.TextChoices):
    LEARNING = "learning", "обучение"
    BEHAVIOR = "behavior", "поведение"
    GENERAL = "general", "общее"
    PARENTS = "parents", "родители"


class UserRole(models.TextChoices):
    ADMIN = "admin", "Администратор"
    MANAGER = "manager", "Менеджер"
    USER = "user", "Пользователь"


TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.all_timezones]
