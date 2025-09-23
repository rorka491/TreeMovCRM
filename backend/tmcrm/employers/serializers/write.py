from rest_framework import serializers
from mainapp.serializers import BaseWriteSerializer
from employers.models import Department, Teacher, Employer


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
