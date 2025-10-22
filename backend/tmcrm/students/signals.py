from django.db.models.signals import post_migrate, post_save, post_delete
from django.dispatch import receiver
from .models import Accrual

@receiver(post_save, sender=Accrual)
def add_student_points(sender, instance, created, **kwargs): 
    if created:
        student = instance.student
        student.score += instance.amount
        if student.score < 0: 
            student.score = 0
        student.save()







