from datetime import timedelta
from django.db import models
from django.core.exceptions import ValidationError
from mainapp.models import BaseModelOrg
from mainapp.validators import phone_number_regex
from mainapp.utils import get_org_local_datetime
from .constants import AccuralCategory

class StudentManager(models.Manager):

    def active(self):
        return self.filter(is_active=True)


class Student(BaseModelOrg):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    phone_number = models.CharField(max_length=11, validators=[phone_number_regex], null=True, blank=True)
    birthday = models.DateField()
    email = models.EmailField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    score = models.IntegerField(default=0)


    class Meta: 
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return self.name

class Parent(BaseModelOrg):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=11, 
        validators=[phone_number_regex],
        blank=True
    )
    child = models.ManyToManyField(Student, related_name='parents')

    class Meta: 
        verbose_name = 'Родитель'
        verbose_name_plural = 'Родители'


    def __str__(self):
        return f'{self.name} {self.surname}'


class StudentGroup(BaseModelOrg):
    name = models.CharField(max_length=100, verbose_name='Название группы', unique=True)
    students = models.ManyToManyField(Student, related_name='groups')
    

    class Meta:
        verbose_name = 'Группа студентов'
        verbose_name_plural = 'Группы студентов'

    def __str__(self):
        return self.name

class Subscription(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subscriptions')
    price = models.DecimalField(max_digits=10, decimal_places=0)
    start_date = models.DateField()
    end_date = models.DateTimeField()
    due_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta: 
        verbose_name = 'Абонемент'
        verbose_name_plural = 'Абонементы'

    def save(self, *args, **kwargs):
        days = kwargs.get('days')

        if not self.end_date:
            if days:
                try:
                    self.end_date = self.start_date + timedelta(days=days)
                except Exception as exc:
                    raise ValidationError('Параметр "days" должен быть числом.') from exc
            else:
                raise ValueError('не передан период days')

        super().save(*args, **kwargs)


class StudentsSnapshot(BaseModelOrg):
    date = models.DateField()
    total_clients = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Снимок учеников"
        verbose_name_plural = "Снимки учеников"

    def __str__(self) -> str:
        return f"Снапшот {self.pk}"

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = get_org_local_datetime(self.get_org).date()
        super().save(*args, **kwargs)


class Accrual(BaseModelOrg):
    amount = models.IntegerField(verbose_name="Количество баллов")
    teacher_profile = models.ForeignKey(
        "mainapp.TeacherProfile",
        on_delete=models.CASCADE,
        related_name="accruals",
        verbose_name="Профиль преподавателя",
    )
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
    )
    category = models.CharField(
        max_length=30, 
        choices=AccuralCategory, 
        default=AccuralCategory.ATTENDANCE,
        verbose_name="Категория начисления", 
    )
    comment = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = "Начисление баллов"
        verbose_name_plural = "Начисления баллов"


