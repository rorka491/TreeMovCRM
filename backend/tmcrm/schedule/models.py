from django.db import models
from students.models import *
from employers.models import *
from django.core.exceptions import ValidationError
from datetime import datetime

WEEK_DAY_CHOICES = (
    (0, "Monday"),
    (1, "Tuesday"),
    (2, "Wednesday"),
    (3, "Thursday"),
    (4, "Friday"),
    (5, "Saturday"),
    (6, "Sunday"),
)

GRADE_CHOICES = (
    (2, 'Неудовлетварительно'),
    (3, 'Удовлетварительно'),
    (4, 'Хорошо'),
    (5, 'Отлично'),
)

class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ManyToManyField(Teacher)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
    
    def __str__(self):
        return self.name


class Schedule(models.Model):
    title = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField(default='2025-01-01')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="schedules")
    week_day = models.PositiveSmallIntegerField(blank=False)
    classroom = models.CharField(max_length=100, default='Not assigned', blank=True, null=True)
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='schedules', blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    is_canceled = models.BooleanField(default=False, blank=True)
    is_completed = models.BooleanField(default=False, blank=True)


    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятие"
        ordering = ["date", "start_time"]

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Конечное время должно быть позже начального")
        super().clean()

    def save(self, *args, **kwargs):
        if self.date:
            self.week_day = self.date.weekday()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.teacher} {self.title} {self.subject}'
    


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    lesson = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='attendances')
    was_present = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'Посещение'
        verbose_name_plural = 'Посещения'

    def __str__(self):
        return f'{self.student.name} присутствовал на {self.lesson.date} по предмету {self.lesson.subject}' if self.was_present else f'{self.student.name} не присутствовал на {self.lesson.date} по предмету {self.lesson.subject}'

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    lesson = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='grades')
    value = models.IntegerField(choices=GRADE_CHOICES, null=True, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        constraints = [
            models.UniqueConstraint(fields=['student', 'lesson'], name='unique_student_lesson_grade')
        ]
    
    def __str__(self):
        return f'{self.value} оценка ученика {self.student.name} за {self.updated_at if self.updated_at else self.created_at}'
    
    def save(self, *args, **kwargs):
        was_present = Attendance.objects.filter(
            student=self.student,
            lesson=self.lesson,
            was_present=True
        ).exists()

        if not was_present:
            raise ValueError('Нельзя поставить оценку: студент не присутствовал на занятии.')
        

        return super().save(*args, **kwargs)

