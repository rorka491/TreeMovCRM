from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from .models import DocumentsTypes, LeaveRequest, Leave
from mainapp.models import Organization
from mainapp.utils import checkout_table 



@receiver(post_migrate)
@checkout_table # Проверка что такая таблица есть
def create_default_document_types(sender, **kwargs):
    if sender.name != 'employers':
        return
    
    defaults = ['Паспорт', 'Договор', 'Снилс', 'Другое']
    for title in defaults:
        DocumentsTypes.objects.get_or_create(title=title)



@receiver(post_save, sender=LeaveRequest)
def create_leave_on_approval(sender, instance: LeaveRequest, created, **kwargs):
    if instance.is_approved:
        Leave.objects.get_or_create(
            leave_request=instance,
            defaults={
                "employee": instance.employee,
                "leave_type": instance.leave_type,
                "start_date": instance.start_date,
                "end_date": instance.end_date,
            }
        )


