from typing import TYPE_CHECKING
from celery import shared_task
from mainapp.utils import get_org_local_datetime, get_cache, CacheType
from mainapp.utils import CacheType
from .models import Student, StudentsSnapshot
from mainapp.models import OrgSettings
from mainapp.utils import get_org_local_datetime

if TYPE_CHECKING:
    from mainapp.models import Organization

@shared_task
def save_clients_snapshot(orgs=None):

    results = []

    if not orgs:
        orgs: list["Organization"] = get_cache(
            "mainapp.Organization", cache_type=CacheType.MODEL
        )

    for org in orgs:
        students_count = Student.objects.filter_by_org(org).count()
        snapshot = StudentsSnapshot.objects.create(
            org=org, 
            total_clients=students_count, 
        )
        results.append(f'Создан снапшот, количество клиентов {students_count}')

    return results