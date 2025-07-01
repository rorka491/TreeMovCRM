from functools import wraps
from django.db.models.signals import post_migrate, post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from mainapp.utils import checkout_table
from .models import SubjectColor
from .models import User, UserSettings, Organization, OrgSettings


colors = [
    ("#FF0000", "Красный"),
    ("#008000", "Зелёный"),
    ("#0000FF", "Синий"),
    ("#FFFF00", "Жёлтый"),
    ("#FFA500", "Оранжевый"),
    ("#800080", "Фиолетовый"),
    ("#FFC0CB", "Розовый"),
    ("#00BFFF", "Голубой"),
    ("#8B4513", "Коричневый"),
    ("#808080", "Серый"),
    ("#000000", "Чёрный"),
    ("#32CD32", "Лаймовый"),
    ("#F5F5DC", "Бежевый"),
    ("#40E0D0", "Бирюзовый"),
    ("#4B0082", "Индиго"),
    ("#FFD700", "Золотой"),
    ("#C0C0C0", "Серебристый"),
    ("#808000", "Оливковый"),
]



# Создавет в базе данных готовые цвета которые пользователь
# сможет использовать чтобы помечать предметы цветами
@receiver(post_migrate)
@checkout_table # проверка что такая таблица есть
def create_colors_preset(sender, **kwargs):
    if sender.name != 'mainapp':
        return

    
    for color, title in colors:
        SubjectColor.objects.get_or_create(color_hex=color, org=None, title=title)


# При создании нового пользователя создает его настройки
@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        if instance.org:
            UserSettings.create_with_user_org(user=instance)
        else:
            UserSettings.create_with_create_by(user=instance)


# При создании новой организации создает настройки организации
@receiver(post_save, sender=Organization)
def create_org_settings(sender, instance, created, **kwargs):
    if created:
        OrgSettings.objects.create(org=instance)

# Обновляет кеш организаций
@receiver([post_save, post_delete], sender=Organization)
def clear_orgs_cache(sender, instance=None, **kwargs):
    orgs = list(sender.objects.all())
    cache.set('orgs', orgs)
