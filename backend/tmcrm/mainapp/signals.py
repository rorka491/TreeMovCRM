from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import SubjectColor
from mainapp.utils import get_orgs

colors = [
    "#FF0000",  # Красный
    "#008000",  # Зелёный
    "#0000FF",  # Синий
    "#FFFF00",  # Жёлтый
    "#FFA500",  # Оранжевый
    "#800080",  # Фиолетовый
    "#FFC0CB",  # Розовый
    "#00BFFF",  # Голубой
    "#8B4513",  # Коричневый
    "#808080",  # Серый
    "#000000",  # Чёрный
    "#FFFFFF",  # Белый
    "#32CD32",  # Лаймовый
    "#F5F5DC",  # Бежевый
    "#40E0D0",  # Бирюзовый
    "#4B0082",  # Индиго
    "#FFD700",  # Золотой
    "#C0C0C0",  # Серебристый
    "#808000",  # Оливковый
]


# Декоратор который передает в функцию дополнительный 
# позиционный аргумент 
def request_orgs(func):
    def wrap(*args, **kwargs):
        kwargs['orgs'] = get_orgs()
        return func(*args,**kwargs)
    return wrap


@receiver(post_migrate)
def create_colors_preset(sender, orgs, **kwargs):
    if sender.name != 'mainapp':
        return
    

    for color in colors:
        SubjectColor.objects.get_or_create(color_hex=color)

