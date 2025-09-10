from mainapp.serializers import BaseWriteSerializer, ColorSerializer, BaseReadSerializer
from students.models import Student, StudentGroup
from lesson_schedule.models import (
    Attendance,
    Classroom,
    Grade,
    Schedule,
    Subject,
    PeriodSchedule,
)
from mainapp.models import SubjectColor
from students.serializers.read import StudentGroupReadSerializer, StudentReadSerializer
from employers.serializers.read import TeacherReadSerializer


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


class ScheduleReadSerializer(BaseReadSerializer):
    teacher = TeacherReadSerializer()
    subject = SubjectReadSerializer(exclude_fields=["teacher"])
    group = StudentGroupReadSerializer(exclude_fields=["students"])
    classroom = ClassroomReadSerializer()

    class Meta(BaseReadSerializer.Meta):
        model = Schedule


class PeriodScheduleReadSerializer(BaseReadSerializer):
    teacher = TeacherReadSerializer()
    subject = SubjectReadSerializer()
    group = StudentGroupReadSerializer(exclude_fields=["students"])
    classroom = ClassroomReadSerializer()

    class Meta(BaseReadSerializer.Meta):
        model = PeriodSchedule


class GradeReadSerializer(BaseReadSerializer):
    student = StudentReadSerializer
    lesson = ScheduleReadSerializer(
        un_exclude_fields=["subject", "date", "teacher", "group"]
    )

    class Meta(BaseReadSerializer.Meta):
        model = Grade
        exclude = ["updated_at"] # Возможно проблема
