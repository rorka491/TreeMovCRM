# В файлах tasks располагаются фоновые процессы
from celery import shared_task
from mainapp.utils import get_org_local_datetime
from mainapp.utils import get_cache
from .models import Schedule


@shared_task
def update_complete_lessons(orgs=None):
    results = []

    if not orgs:
        orgs = get_cache('orgs')

    for org in orgs:
        current_time = get_org_local_datetime(org).time()
        current_date = get_org_local_datetime(org).date()

        lessons = Schedule.objects.filter(
            org=org, 
            end_time__lte=current_time,
            date__lte=current_date,
            is_completed=False
        )

        updated = lessons.update(is_completed=True)
        results.append(f"{updated} урок(ов) обновлено для организации {org.name}")
    return results
