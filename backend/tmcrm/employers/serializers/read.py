from rest_framework import serializers
from employers.models import Teacher, Employer, Department
from mainapp.serializers import BaseReadSerializer


class EmployerReadSerializer(BaseReadSerializer):

    class Meta(BaseReadSerializer.Meta):
        model = Employer


class TeacherReadSerializer(BaseReadSerializer):
    employer = EmployerReadSerializer()

    class Meta(BaseReadSerializer.Meta):
        model = Teacher


class DepartmentReadSerializer(BaseReadSerializer):

    class Meta(BaseReadSerializer.Meta):
        model = Department
