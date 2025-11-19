import django_filters
from lesson_schedule.models import Attendance, Grade, Lesson
from students.models import Student, StudentsSnapshot, StudentGroup
from mainapp.filters import DateRangeMixin


class AttendanceFilter(django_filters.FilterSet):                          
    group = django_filters.ModelMultipleChoiceFilter(
        field_name="student__groups",
        queryset=StudentGroup.objects.all(),
        to_field_name="id",
        label="Группа",
    )
    start_date = django_filters.DateFilter(lookup_expr="gte", field_name="lesson_date")
    end_date = django_filters.DateFilter(lookup_expr="lte", field_name="lesson_date")
    lesson_date = django_filters.DateFilter()

    class Meta:
        model = Attendance
        fields = '__all__'


class GradeFilter(django_filters.FilterSet):
    group = django_filters.ModelChoiceFilter(
        field_name="student__groups",
        queryset=StudentGroup.objects.all(),
        to_field_name="id",
        label="Группа",
    )
    start_date = django_filters.DateFilter(lookup_expr="gte", field_name="grade_date")
    end_date = django_filters.DateFilter(lookup_expr="lte", field_name="grade_date")
    grade_date = django_filters.DateFilter()

    class Meta:
        model = Grade
        fields = "__all__"


class StudentSnapshotFilter(django_filters.FilterSet):

    class Meta:
        model = StudentsSnapshot
        fields = ['date']

class LessonFilter(DateRangeMixin, django_filters.FilterSet):

    class Meta:
        model = Lesson
        exclude = ["duration"]


class StudentFilter(django_filters.FilterSet):
    group = django_filters.ModelMultipleChoiceFilter(
        field_name="student__groups",
        queryset=StudentGroup.objects.all(),
        to_field_name="id",
        label="Группа",
    )

    class Meta:
        model = Student
        fields = ["group", ]