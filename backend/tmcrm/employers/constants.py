from django.db import models

class NoteCategory(models.TextChoices):
    LEARNING = "learning", "обучение"
    BEHAVIOR = "behavior", "поведение"
    GENERAL = "general", "общее"
    PARENTS = "parents", "родители"


