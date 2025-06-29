from django.apps import AppConfig


class LessonScheduleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lesson_schedule'

    def ready(self):
        import lesson_schedule.signals

