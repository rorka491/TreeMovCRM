from functools import wraps
from django.db.models.signals import post_migrate, post_save, post_delete
from django.dispatch import receiver
from .utils import checkout_table, checkout_interval_schedule_table, delete_cache
from .models import User, UserSettings, Organization, OrgSettings, SubjectColor


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


# При создании нового пользователя создает его настройки и присваивает организацию
@receiver(post_save, sender=User)
def create_user_settings_with_org(sender, instance, created, **kwargs):
    if created and not instance.is_superuser and instance.org:
        UserSettings.objects.create(
            user=instance, 
            org=instance.get_org(), 
            created_by=instance
        )

# При создании нового пользователя создает его настройки без присваения организации
@receiver(post_save, sender=User)
def create_user_settings_without_org(sender, instance, created, **kwargs):
    if created and not instance.is_superuser and not instance.org:
        UserSettings.objects.create(
            user=instance, created_by=instance
        )


# При создании новой организации создает настройки организации
@receiver(post_save, sender=Organization)
def create_org_settings(sender, instance, created, **kwargs):
    if created:
        OrgSettings.create_manager.create(
            org=instance, 
            created_by=instance.created_by 
        )
        created_by = instance.created_by
        User.objects.filter(username=created_by).update(org=instance)



# Обновляет кеш организаций
@receiver([post_save, post_delete], sender=Organization)
def clear_orgs_cache_on_save(sender, instance=None, **kwargs):
    delete_cache('mainapp.Organization')

# Инициализирует задачи Celery
@receiver(post_migrate)
@checkout_interval_schedule_table
def setup_periodic_tasks(sender, **kwargs):
    from lesson_schedule.utils import (
        init_task_create_update_complete_lessons_task,
        init_task_create_attendences_for_all_passes,
    )
    from students.utils import init_task_save_clients_snapshot

    init_task_create_update_complete_lessons_task()
    init_task_create_attendences_for_all_passes()
    init_task_save_clients_snapshot()
