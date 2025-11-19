import django_filters
from lesson_schedule.models import Attendance, Grade, Lesson
from students.models import Student, StudentsSnapshot, StudentGroup
from mainapp.filters import DateRangeMixin


class LessonFilter(DateRangeMixin, django_filters.FilterSet):

    class Meta:
        model = Lesson
        exclude = ["duration"]
