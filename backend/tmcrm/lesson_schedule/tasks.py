# В файлах tasks располагаются фоновые процессы
from celery import shared_task
from mainapp.utils import get_org_local_time
from .models import Schedule
from mainapp.models import Organization
from tmcrm.celery import app
from mainapp.utils import get_orgs


@shared_task
def update_complete_lessons(orgs=None):
    results = []

    if not orgs:
        orgs = get_orgs()
        
    for org in orgs:
        current_time = get_org_local_time(org).time()
        current_date = get_org_local_time(org).date()

        print(f"Org: {org.name}, current_date: {current_date}, current_time: {current_time}")

        lessons = Schedule.objects.filter(
            org=org, 
            end_time__lte=current_time,
            date__lte=current_date,
            is_completed=False
        )

        updated = lessons.update(is_completed=True)
        results.append(f"{updated} урок(ов) обновлено для организации {org.name}")
    return results




