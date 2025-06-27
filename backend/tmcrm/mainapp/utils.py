from .models import Organization, OrgSettings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from functools import wraps
from django.db import connection
from django.db.utils import OperationalError
from functools import wraps
from django.apps import AppConfig
from functools import total_ordering
from datetime import date, datetime
import pytz
from django.utils import timezone
from django.db import connection, ProgrammingError, OperationalError


#Кэшированные оргинзации
_orgs_cache = None 


def get_orgs():
    """Метод для получения оганизаций
    кеширование реализовано чтобы минимизировать количесвто 
    запросов к базе
    Если в каком либо методе надо получить организации то делается это церез
    request_orgs который лежит в mainapp.signals
    Пример: 
    @request_orgs
    some_func(orgs=None)
        Дальше используйте orgs как хотите
    """
    
    global _orgs_cache
    if _orgs_cache is None:
        _orgs_cache = Organization.objects.all()
    return _orgs_cache


def get_org_local_time(org):
    """"Функция возвращает локальное время для заданной организации"""

    tz = pytz.timezone(org.orgsettings.first().timezone)
    return timezone.now().astimezone(tz)
    

@receiver([post_save, post_delete], sender=Organization)
def clear_orgs_cache(sender, **kwargs):
    global _orgs_cache
    _orgs_cache = None  # Сбрасываем кеш, чтобы он обновился при следующем вызове

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
        raise TypeError(f'Получен класс не поддерживающийся для конвертации ожидалось date, datetime, DateFieldExcludeYear')

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
    """Декоратор используется для сигналов которые использзуются через
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