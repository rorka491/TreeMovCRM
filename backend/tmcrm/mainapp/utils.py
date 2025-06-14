from .models import Organization
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


#Кэшированные оргинзации
_orgs_cache = None 


def get_orgs():
    """Метод для получения оганизаций"""
    global _orgs_cache
    if _orgs_cache is None:
        _orgs_cache = Organization.objects.all()
    return _orgs_cache


@receiver([post_save, post_delete], sender=Organization)
def clear_orgs_cache(sender, **kwargs):
    global _orgs_cache
    _orgs_cache = None  # Сбрасываем кеш, чтобы он обновился при следующем вызове

