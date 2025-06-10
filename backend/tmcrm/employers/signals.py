from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import DocumentsTypes 
from mainapp.models import Organization

@receiver(post_migrate)
def create_default_document_types(sender, **kwargs):
    if sender.name != 'employers':
        return
    
    defaults = ['Паспорт', 'Договор', 'Снилс', 'Другое']
    orgs = Organization.objects.all()
    for org in orgs:
        for title in defaults:
            DocumentsTypes.objects.get_or_create(title=title, org=org)
