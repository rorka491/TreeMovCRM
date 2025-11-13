# В файлах tasks располагаются фоновые процессы
from celery import shared_task
from mainapp.utils import get_org_local_datetime, get_cache, CacheType
from mainapp.models import Organization 
from django.db import transaction
from .models import Lesson, Attendance
from .utils import _get_complited_lessons_for_org, _create_missing_attendances_for_lesson


@shared_task
def update_complete_lessons(orgs=None):
    results = []

    if not orgs:
        orgs: list[Organization] = get_cache("mainapp.Organization", cache_type=CacheType.MODEL)

    for org in orgs:
        current_time = get_org_local_datetime(org).time()
        current_date = get_org_local_datetime(org).date()
        print(f'\n{current_time}, {current_date}')

        lessons = Lesson.objects.filter_by_org(org=org).filter(
            end_time__lte=current_time,
            date__lte=current_date,
            is_completed=False,
        )

        updated = lessons.update(is_completed=True)
        if updated > 0:
            results.append(f"{updated} урок(ов) обновлено для организации {org.name}")
    return "\nРезультатов нет" if not results else results


@shared_task
def create_attendences_for_all_passes(orgs=None):
    results = []

    if not orgs:
        orgs: list[Organization] = get_cache("mainapp.Organization", cache_type=CacheType.MODEL)

    for org in orgs:
        lessons = _get_complited_lessons_for_org(org=org)

        for lesson in lessons:
            if not lesson.group:
                continue

            attendances = _create_missing_attendances_for_lesson(lesson=lesson)
            if len(attendances) > 0 :
                Attendance.objects.bulk_create(attendances)
                results.append({"lesson_id": lesson.id, "created": len(attendances)})

    return "\nРезультатов нет" if not results else results
