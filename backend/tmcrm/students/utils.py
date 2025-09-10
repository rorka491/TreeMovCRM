from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json


def init_task_save_clients_snapshot():
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1, period=IntervalSchedule.DAYS
    )

    PeriodicTask.objects.update_or_create(
        name="Создание снапшота клиентов для каждой организации",
        defaults={
            "interval": schedule,
            "task": "students.tasks.save_clients_snapshot",
            "args": json.dumps([]),
            "kwargs": json.dumps({}),
        },
    )
