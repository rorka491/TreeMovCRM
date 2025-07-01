from functools import wraps, total_ordering
from datetime import date, datetime
import inspect
import pytz
from django.db import connection, ProgrammingError, OperationalError
from django.apps import AppConfig
from django.core.cache import cache
from django.utils import timezone
from .models import Organization, OrgSettings


def get_cache(key):
    return cache.get(key)

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
        orgs = get_cache("orgs")

        # Проверяем, принимает ли функция параметр orgs
        sig = inspect.signature(func)
        if "orgs" in sig.parameters:
            kwargs["orgs"] = orgs

        return func(*args, **kwargs)

    return wrap


@total_ordering
class DateFieldExcludeYear():
    """Класс нужен для того что бы исопльзовать 
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
