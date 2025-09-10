import django_filters
from lesson_schedule.models import Attendance, Grade, Schedule
from students.models import Student, StudentsSnapshot, StudentGroup
from employers.models import Teacher
from mainapp.filters import DateRangeMixin

# filters
class AttendanceFilter(DateRangeMixin, django_filters.FilterSet):
    group = django_filters.ModelChoiceFilter(
        field_name="student__groups",
        queryset=StudentGroup.objects.all(),
        label="Группа",
    )
    date_field = "lesson_date"

    class Meta:
        model = Attendance
        fields = "__all__"


class GradeFilter(DateRangeMixin, django_filters.FilterSet):
    group = django_filters.ModelChoiceFilter(
        field_name="student__groups",
        queryset=StudentGroup.objects.all(),
        label="Группа",
    )
    date_field = "grade_date"

    class Meta:
        model = Grade
        fields = "__all__"


class StudentSnapshotFilter(django_filters.FilterSet):
    

    class Meta:
        model = StudentsSnapshot
        fields = "__all__"

class LessonFilter(DateRangeMixin, django_filters.FilterSet):

    class Meta:
        model = Schedule
        fields = "__all__"
