from django.db import models
from mainapp.models import SubjectColor
from students.models import *
from employers.models import *
from django.core.exceptions import ValidationError
from datetime import date

WEEK_DAY_CHOICES = (
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
)

GRADE_CHOICES = (
    (2, "Не удовлетварительно"),
    (3, "Удовлетварительно"),
    (4, "Хорошо"),
    (5, "Отлично"),
)


class Subject(BaseModelOrg):
    name = models.CharField(max_length=100)
    teacher = models.ManyToManyField(Teacher)
    color = models.ForeignKey(
        SubjectColor, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        super().clean()

        qs = Subject.objects.filter(org=self.org, color=self.color)

        if self.pk:
            qs = qs.exclude(pk=self.pk)

        if qs.exists():
            raise ValidationError(
                {
                    "color": "Этот цвет уже используется для другого предмета в вашей организации."
                }
            )


class Classroom(BaseModelOrg):
    title = models.CharField(max_length=100)
    floor = models.SmallIntegerField(null=True, blank=True)
    building = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Аудитория"
        verbose_name_plural = "Аудиории"

    def __str__(self):
        return f"Аудитория {self.title}"


class PeriodSchedule(BaseModelOrg):
    """Специльный класс для периодических занятий"""

    period = models.PositiveSmallIntegerField(blank=True, null=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="period_schedules",
        null=True,
        blank=True,
    )
    classroom = models.ForeignKey(
        Classroom,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="period_schedules",
    )
    group = models.ForeignKey(
        StudentGroup,
        on_delete=models.CASCADE,
        related_name="period_schedules",
        blank=True,
        null=True,
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, null=True, blank=True
    )
    lesson = models.PositiveSmallIntegerField(blank=True, null=True)
    repeat_lessons_until_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Периодическое занятие"
        verbose_name_plural = "Периодические занятия"


class Schedule(BaseModelOrg):
    """Класс для всех занятий в том числе и периодических"""

    title = models.CharField(max_length=100, blank=True)
    date = models.DateField(default=date.today())
    week_day = models.PositiveSmallIntegerField(blank=False)
    is_canceled = models.BooleanField(default=False, blank=True)
    is_completed = models.BooleanField(default=False, blank=True)

    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="schedules"
    )
    classroom = models.ForeignKey(
        Classroom,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="schedules",
    )
    group = models.ForeignKey(
        StudentGroup,
        on_delete=models.CASCADE,
        related_name="schedules",
        blank=True,
        null=True,
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, null=True, blank=True
    )
    lesson = models.PositiveSmallIntegerField(blank=True, null=True)

    period_schedule = models.ForeignKey(
        PeriodSchedule, on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"
        ordering = ["date", "start_time"]

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Конечное время должно быть позже начального")

        filters = {
            "date": self.date,
            "lesson": self.lesson,
        }

        if self.pk:
            exclude = {"pk": self.pk}
        else:
            exclude = {}

        teacher_qs = Schedule.objects.filter(teacher=self.teacher, **filters).exclude(
            **exclude
        )
        group_qs = Schedule.objects.filter(group=self.group, **filters).exclude(
            **exclude
        )

        if teacher_qs.exists():
            raise ValidationError("У этого преподавателя на эту пару и дату занятие")
        if group_qs.exists():
            raise ValidationError("У этой группы на эту пару и дату занятие")

        super().clean()

    def save(self, *args, **kwargs):
        if self.date:
            self.week_day = self.date.isoweekday()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.teacher} {self.title} {self.subject}"


class Attendance(BaseModelOrg):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="attendances"
    )
    lesson = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name="attendances"
    )
    was_present = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Посещение"
        verbose_name_plural = "Посещения"

    def __str__(self):
        return (
            f"{self.student.name} присутствовал на {self.lesson.date} по предмету {self.lesson.subject}"
            if self.was_present
            else f"{self.student.name} не присутствовал на {self.lesson.date} по предмету {self.lesson.subject}"
        )


class Grade(BaseModelOrg):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="grades"
    )
    lesson = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name="grades"
    )
    value = models.IntegerField(choices=GRADE_CHOICES, null=True, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        constraints = [
            models.UniqueConstraint(
                fields=["student", "lesson"], name="unique_student_lesson_grade"
            )
        ]

    def __str__(self):
        return f"{self.value} оценка ученика {self.student.name} за {self.updated_at if self.updated_at else self.created_at}"

    def save(self, *args, **kwargs):
        was_present = Attendance.objects.filter(
            student=self.student, lesson=self.lesson, was_present=True
        ).exists()

        if not was_present:
            raise ValueError(
                "Нельзя поставить оценку: студент не присутствовал на занятии."
            )

        return super().save(*args, **kwargs)
