from rest_framework import serializers
from employers.models import Teacher
from students.models import Student, StudentGroup
from lesson_schedule.models import (
    Attendance,
    Classroom,
    Schedule,
    Subject,
    PeriodSchedule,
    Grade,
)
from mainapp.models import SubjectColor
from mainapp.serializers import BaseWriteSerializer, ColorSerializer


class ClassroomWriteSerializer(BaseWriteSerializer):

    class Meta(BaseWriteSerializer.Meta):
        model = Classroom


class SubjectWriteSerializer(BaseWriteSerializer):
    color = serializers.PrimaryKeyRelatedField(queryset=SubjectColor.objects.all())

    class Meta(BaseWriteSerializer.Meta):
        model = Subject


class AttendanceWriteSerializer(BaseWriteSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    lesson = serializers.PrimaryKeyRelatedField(queryset=Schedule.objects.all())

    class Meta(BaseWriteSerializer.Meta):
        model = Attendance


class ScheduleWriteSerializer(BaseWriteSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=StudentGroup.objects.all())
    classroom = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())

    class Meta(BaseWriteSerializer.Meta):
        model = Schedule
        exclude_fields = ['week_day']


class PeriodScheduleWriteSerializer(BaseWriteSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=StudentGroup.objects.all())
    classroom = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())

    class Meta(BaseWriteSerializer.Meta):
        model = PeriodSchedule


class GradeWriteSerializer(BaseWriteSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    lesson = serializers.PrimaryKeyRelatedField(queryset=Schedule.objects.all())

    class Meta(BaseWriteSerializer.Meta):
        model = Grade   
