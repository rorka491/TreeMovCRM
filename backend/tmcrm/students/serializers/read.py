from lesson_schedule.models import Attendance
from mainapp.serializers import BaseReadSerializer
from students.models import StudentGroup, Student, Parent, Accrual
from mainapp.models import TeacherProfile
from rest_framework import serializers
from mainapp.serializers import BaseReadSerializer


class StudentReadSerializer(BaseReadSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=StudentGroup.objects.all()
    )

    class Meta(BaseReadSerializer.Meta):
        model = Student


class StudentGroupReadSerializer(BaseReadSerializer):
    students = StudentReadSerializer(
        exclude_fields=["groups"],
        many=True,
    )

    class Meta(BaseReadSerializer.Meta):
        model = StudentGroup


class ParentReadSerializer(BaseReadSerializer):
    child = StudentReadSerializer(many=True, read_only=True, exclude_fields=["groups"])

    class Meta(BaseReadSerializer.Meta):
        model = Parent


class AccrualReadSerializer(BaseReadSerializer):
    teacher_profile = serializers.PrimaryKeyRelatedField(
        queryset=TeacherProfile.objects.all()
    )
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())

    class Meta(BaseReadSerializer.Meta):
        model = Accrual
