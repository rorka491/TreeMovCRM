from django.db import models


class AccuralCategory(models.TextChoices):
    ATTENDANCE = "attendance", "Посещаемость"
    PARTICIPATION = "participation", "Участие"
    BEHAVIOR = "behavior", "Поведение"
    ACHIEVEMENTS = "achievements", "Достижения"
    HOMEWORK = "homework", "Домашнее задание"

