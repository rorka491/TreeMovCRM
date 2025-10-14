from django.db import models
from mainapp.models import BaseModelOrg, Organization


class Department(BaseModelOrg):
    title = models.CharField(max_length=100, )
    code = models.IntegerField()

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

class Employer(BaseModelOrg):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    passport_series = models.CharField(max_length=4, null=True, blank=True) 
    passport_num = models.CharField(max_length=6, null=True, blank=True)      
    inn = models.CharField(max_length=12, null=True, blank=True) 
    
    class Meta: 
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'Сотрудник {self.name, self.surname}'


class Teacher(BaseModelOrg):
    employer = models.OneToOneField(Employer, on_delete=models.CASCADE)

    class Meta: 
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        
    def __str__(self):
        return f'{self.employer.name} {self.employer.surname}'

class JobTitle(BaseModelOrg):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class LeaveType(models.TextChoices):
    VACATION = "vacation", "Отпуск"
    SICK = "sick", "Больничный"
    UNPAID = "unpaid", "За свой счет"

class LeaveStatus(models.TextChoices):
    PENDING = 'pending', 'Ожидает'
    APPROVED = "approved", "Одобрено"
    REJECTED =   "rejected", "Отклонено"

class LeaveRequest(BaseModelOrg):
    employee = models.ForeignKey(Employer, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LeaveType.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=LeaveStatus.choices, default=LeaveStatus.PENDING
    )

    class Meta:
        verbose_name = 'Запросы на отпуск'
        verbose_name_plural = "Запросы на отпуск"

    def __str__(self) -> str:
        return f'{self.leave_type}'

    @property
    def is_approved(self) -> bool:
        return self.status == LeaveStatus.APPROVED

class Leave(BaseModelOrg): 
    leave_request = models.OneToOneField(LeaveRequest, on_delete=models.CASCADE)
    employee = models.ForeignKey("Employer", on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LeaveType.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    comment= models.TextField(null=True)
    documents = models.ManyToManyField("Documents", related_name='leaves')

    class Meta:
        verbose_name = "Отпуск"
        verbose_name_plural = "Отпуска"

    def __str__(self):
        return (
            f"{self.employee} — {self.leave_type} ({self.start_date} → {self.end_date})"
        )

class DocumentsTypes(BaseModelOrg):
    """
    Класс тип документа
    Переопределен org так как он должен допускать по умолчанию 
    значение default
    """
    title = models.CharField(max_length=100)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)


    class Meta: 
        verbose_name = 'Тип документа'
        verbose_name_plural = 'Типы документов'

    def __str__(self):
        return f'{self.title}'


class Documents(BaseModelOrg):
    from mainapp.models import User

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    file_path = models.FileField(upload_to='documents/')
    upload_at = models.DateTimeField(auto_now_add=True)
    access_to_document = models.ManyToManyField(User) 
    doc_type = models.ForeignKey(DocumentsTypes, on_delete=models.CASCADE, blank=True, null=True)
    

    class Meta: 
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
