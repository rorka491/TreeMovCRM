from rest_framework import serializers
from mainapp.serializers import BaseWriteSerializer
from employers.models import Department, Teacher, Employer, Leave, TeacherNote
from mainapp.models import TeacherProfile

class EmployerWriteSerializer(BaseWriteSerializer):

    class Meta(BaseWriteSerializer.Meta):
        model = Employer


class TeacherWriteSerializer(BaseWriteSerializer):
    employer = serializers.PrimaryKeyRelatedField(queryset=Employer.objects.all())

    class Meta(BaseWriteSerializer.Meta):
        model = Teacher


class DepartmentWriteSerializer(BaseWriteSerializer):

    class Meta(BaseWriteSerializer.Meta):
        model = Department


class LeaveWriteSerializer(BaseWriteSerializer):

    class Meta(BaseWriteSerializer.Meta):
        model = Leave

class TeacherNoteWriteSerializer(BaseWriteSerializer):

    class Meta(BaseWriteSerializer.Meta):
        model = TeacherNote
        read_only_fields = ["teacher_profile"]


class TeacherProfileWriteSerializer(BaseWriteSerializer):

    class Meta(BaseWriteSerializer.Meta):
        model = TeacherProfile


