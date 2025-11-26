from mainapp.serializers import BaseWriteSerializer, ColorSerializer, BaseReadSerializer
from students.models import Student, StudentGroup
from lesson_schedule.models import (
    Attendance,
    Classroom,
    Grade,
    Lesson,
    Subject,
    PeriodLesson,
)
from mainapp.models import SubjectColor
from students.serializers.read import StudentGroupReadSerializer, StudentReadSerializer
from employers.serializers.read import TeacherReadSerializer
from rest_framework.serializers import SerializerMethodField


class ClassroomReadSerializer(BaseReadSerializer):

    class Meta(BaseReadSerializer.Meta):
        model = Classroom


class SubjectReadSerializer(BaseReadSerializer):
    color = ColorSerializer()

    class Meta(BaseReadSerializer.Meta):
        model = Subject


class AttendanceReadSerializer(BaseReadSerializer):

    class Meta(BaseReadSerializer.Meta):
        model = Attendance


class PeriodScheduleReadSerializer(BaseReadSerializer):
    teacher = TeacherReadSerializer()
    subject = SubjectReadSerializer()
    group = StudentGroupReadSerializer(exclude_fields=["students"])
    classroom = ClassroomReadSerializer()

    class Meta(BaseReadSerializer.Meta):
        model = PeriodLesson

class ScheduleReadSerializer(BaseReadSerializer):
    teacher = TeacherReadSerializer()
    subject = SubjectReadSerializer(exclude_fields=["teacher"])
    group = StudentGroupReadSerializer(exclude_fields=["students"])
    classroom = ClassroomReadSerializer()
    period_lesson = SerializerMethodField()

    class Meta(BaseReadSerializer.Meta):
        model = Lesson

    def get_period_lesson(self, obj: Lesson):
        return PeriodScheduleReadSerializer(obj.period_schedule, un_exclude_fields=['period']).data


class GradeReadSerializer(BaseReadSerializer):
    student = StudentReadSerializer
    lesson = ScheduleReadSerializer(
        un_exclude_fields=["subject", "date", "teacher", "group"]
    )

    class Meta(BaseReadSerializer.Meta):
        model = Grade
        exclude = ["updated_at"] # Возможно проблема
