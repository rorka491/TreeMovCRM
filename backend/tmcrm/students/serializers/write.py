from lesson_schedule.models import Attendance
from mainapp.serializers import BaseWriteSerializer
from rest_framework import serializers
from students.models import StudentGroup, Student, Parent


class StudentWriteSerializer(BaseWriteSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=StudentGroup.objects.all()
    )

    class Meta(BaseWriteSerializer.Meta):
        model = Student


class StudentGroupWriteSerializer(BaseWriteSerializer):
    students = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Student.objects.all(), 
        required=False, default=list
    )

    class Meta(BaseWriteSerializer.Meta):
        model = StudentGroup


class ParentWriteSerializer(BaseWriteSerializer):
    child = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Student.objects.all()
    )

    class Meta(BaseWriteSerializer.Meta):
        model = Parent
