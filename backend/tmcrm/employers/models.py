from django.db import models
from mainapp.models import BaseModelOrg


class Employer(BaseModelOrg):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)


    class Meta: 
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'Сотрудник {self.name, self.surname}'



class Teacher(BaseModelOrg):
    employer = models.OneToOneField(Employer, on_delete=models.CASCADE, primary_key=True)

    class Meta: 
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        
    def __str__(self):
        return f'Преподаватель {self.employer.name, self.employer.surname}'
    
class JobTitle(BaseModelOrg):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = ''
        verbose_name_plural = 'Должности'



class LeaveType(models.TextChoices):
    VACATION = "vacation", "Отпуск"
    SICK = "sick", "Больничный"
    UNPAID = "unpaid", "За свой счет"

class LeaveRequest(BaseModelOrg):
    employee = models.ForeignKey(Employer, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LeaveType.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Ожидает'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ], default='pending')

    created_at = models.DateTimeField(auto_now_add=True)



