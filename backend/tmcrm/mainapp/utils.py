from functools import wraps, total_ordering
from typing import Type
from enum import Enum
from datetime import date, datetime
import inspect
import pytz
from django.apps import apps
from django.db import connection, ProgrammingError, OperationalError, models
from django.apps import AppConfig
from django.core.cache import cache
from django.utils import timezone


class CacheType(str, Enum):
    MODEL = "model"
    OTHER = 'other'


def _get_model(app_model: str) -> Type[models.Model]:
    try:
        app_label, model_name = app_model.split(".")
    except ValueError:
        raise ValueError("Ключ должен быть в формате 'app_label.ModelName'")

    model = apps.get_model(app_label, model_name)
    if model is None:
        raise ValueError(f"Модель '{app_model}' не найдена")

    return model


def get_cache(key: str, cache_type: CacheType='model'):
    """
    Для доступа к моделям и бд
    key должен быть в формате 'app_label.ModelName'
    Например: 'mainapp.Organization' или 'users.User'
    
    """
    result = cache.get(key, None)
    if result is not None:
        return result
    
    match cache_type:
        case 'model':
            model = _get_model(key)
            result = list(model.objects.all())
        case 'other':
            ...
    
    if result is None:
        raise ValueError(f"Не удалось получить значение для ключа: {key} (тип кэша: {cache_type})")

    cache.set(key, result, timeout=0)
    return result


def delete_cache(key):
    cache.delete(key)

def get_org_local_datetime(org):
    """"Функция возвращает локальное время для заданной организации"""

    tz = pytz.timezone(org.settings.timezone)
    return timezone.now().astimezone(tz)


# Декоратор который передает в функцию дополнительный
# позиционный аргумент который получает все возможные организации
def request_orgs(func):
    @wraps
    def wrap(*args, **kwargs):
        orgs = get_cache("mainapp.Organization")

        # Проверяем, принимает ли функция параметр orgs
        sig = inspect.signature(func)
        if "orgs" in sig.parameters:
            kwargs["orgs"] = orgs

        return func(*args, **kwargs)

    return wrap


@total_ordering
class DateFieldExcludeYear():
    """Класс нужен для того что бы использовать 
    date для определения только дня и месяца
    Пример: 
    date = DateFieldExcludeYear(6, 23)
    6 месяц 23 день, год опущен
    """
    def __init__(self, month, day):
        if not (1 <= month <= 12):
            raise ValueError("Месяц должен быть от 1 до 12")
        if not (1 <= day <= 31):
            raise ValueError("День должен быть от 1 до 31")
        
        self.month, self.day = month, day
        
    def __repr__(self):
        return f"{self.month:02d}-{self.day:02d}"
    
    def _as_tuple(self):
        return (self.month, self.day)
    
    def _convert_other(self, other):
        if isinstance(other, DateFieldExcludeYear):
            return self._as_tuple()
        if isinstance(other, (date, datetime)):
            return (other.month, other.day)
        raise TypeError(
            'Получен класс не поддерживающийся для конвертации ожидалось date,' \
            ' datetime, DateFieldExcludeYear')

    def __eq__(self, other):
        try: 
            return self._as_tuple() == self._convert_other(other)
        except TypeError:
            return NotImplemented
        
    def __lt__(self, other):
        try:
            return self._as_tuple() < self._convert_other(other)
        except TypeError:
            return NotImplemented


def checkout_table(func):
    """Декоратор используется для сигналов которые используются через
    post_migrate"""
    @wraps(func)
    def wrapper(sender, **kwargs):
        
        if isinstance(sender, AppConfig):# Проверка чтобы срабатывать когда sender не AppConfig
            return func(sender, **kwargs)
        
        table_name = sender._meta.db_table

        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT 1 FROM {table_name} LIMIT 1;")
        except OperationalError:
            # Таблица не существует, пропускаем создание записей
            return
        return func(sender)
    return wrapper


def checkout_interval_schedule_table(func):
    """Декоратор для сигналов post_migrate — проверяет наличие таблицы IntervalSchedule"""
    @wraps(func)
    def wrapper(sender, **kwargs):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM django_celery_beat_intervalschedule LIMIT 1;")
        except (ProgrammingError, OperationalError):
            # Таблица не существует — не вызываем функцию
            return
        return func(sender, **kwargs)
    return wrapper


