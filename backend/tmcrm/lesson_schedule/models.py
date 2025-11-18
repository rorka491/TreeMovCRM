from datetime import date, datetime
from genericpath import exists
from django.db import models
from django.core.exceptions import ValidationError   
from django.db.models import F, ExpressionWrapper, DurationField
from django.utils import timezone
from employers.models import Teacher
from students.models import StudentGroup, Student
from mainapp.models import SubjectColor, BaseModelOrg

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

        qs = Subject.objects.filter(color=self.color)

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

class AbstrctLesson(BaseModelOrg):
    title = models.CharField(max_length=200)
    start_time = models.TimeField(
        blank=False,
        null=True,
        help_text="Please use the following format: <em>YYYY-MM-DD</em>.",
    )
    end_time = models.TimeField(
        blank=False,
        null=True,
        help_text="Please use the following format: <em>YYYY-MM-DD</em>.",
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="%(class)s_teacher",
        null=True,
        blank=True,
    )
    classroom = models.ForeignKey(
        Classroom,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_group",
    )
    group = models.ForeignKey(
        StudentGroup,
        on_delete=models.CASCADE,
        related_name="%(class)s_classroom",
        blank=True,
        null=True,
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_subject",
    )

    class Meta:
        abstract = True


class PeriodLesson(AbstrctLesson):
    """Специльный класс для периодических занятий"""
    period = models.PositiveSmallIntegerField(blank=True, null=True)
    repeat_lessons_until_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)

    class Meta:
        # db_table = "lesson_schedule_periodlesson"
        verbose_name = "Периодическое занятие"
        verbose_name_plural = "Периодические занятия"


class Lesson(AbstrctLesson):
    """Класс для всех занятий в том числе и периодических"""
    date = models.DateField(default=timezone.now, blank=False)
    week_day = models.PositiveSmallIntegerField(blank=False)
    is_canceled = models.BooleanField(default=False, blank=True)
    is_completed = models.BooleanField(default=False, blank=True)

    period_schedule = models.ForeignKey(
        PeriodLesson, on_delete=models.SET_NULL, blank=True, null=True
    )
    duration = models.DurationField(blank=True, null=True, editable=False)
    comment = models.CharField(max_length=200, blank=True)

    class Meta:
        # db_table = "lesson_schedule_lesson"
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"
        ordering = ["date", "start_time"]

    @property   
    def calc_duration(self):
        """Возвращает timedelta между start_time и end_time"""
        if self.start_time and self.end_time:
            start_dt = datetime.combine(date.today(), self.start_time)
            end_dt = datetime.combine(date.today(), self.end_time)
            return end_dt - start_dt
        return None

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Конечное время должно быть позже начального")

        filters = {
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }


        if self.pk:
            exclude = {"pk": self.pk}
        else:
            exclude = {}

        teacher_qs = Lesson.objects.filter(teacher=self.teacher, **filters).exclude(
            **exclude
        )
        group_qs = Lesson.objects.filter(group=self.group, **filters).exclude(
            **exclude
        )

        if teacher_qs.exists():
            raise ValidationError("У этого преподавателя на пару и дату занятие")
        if group_qs.exists():
            raise ValidationError("У этой группы на эту пару и дату занятие")

        super().clean()

    def save(self, *args, **kwargs):
        if self.date:
            self.week_day = self.date.isoweekday()
        if self.start_time and self.end_time:
            self.duration = self.calc_duration
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.teacher} {self.title} {self.date}"


class Attendance(BaseModelOrg):
    student = models.ForeignKey(
        'students.Student', on_delete=models.CASCADE, related_name="attendances"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="attendances"
    )
    lesson_date = models.DateField(null=True, blank=True)
    was_present = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Посещение"
        verbose_name_plural = "Посещения"


    def clean(self):
        exists = (
            Attendance.objects.filter(student=self.student, lesson=self.lesson)
            .exclude(id=self.id)
            .exists()
        )

        if exists:
            raise ValidationError("Это посещение уже существует.")

        return super().clean()

    def save(self, *args, **kwargs):
        print(
            f"[SAVE] lesson: {self.lesson}, lesson.date: {getattr(self.lesson, 'date', None)}"
        )
        if not self.lesson_date:
            self.lesson_date = self.lesson.date
        super().save(*args, **kwargs)

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
        Lesson, on_delete=models.CASCADE, related_name="grades"
    )
    value = models.IntegerField(choices=GRADE_CHOICES, null=True, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    grade_date = models.DateField(blank=True, null=True)
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
        if self.lesson.date and self.lesson:
            self.grade_date = self.lesson.date
        return super().save(*args, **kwargs)
