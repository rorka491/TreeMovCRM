from rest_framework import serializers
from employers.models import Teacher, Employer, Department, Leave, TeacherNote
from mainapp.serializers import BaseReadSerializer
from mainapp.models import TeacherProfile, User

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


class LeaveReadSerializer(BaseReadSerializer):

    class Meta(BaseReadSerializer.Meta):
        model = Leave


class TeacherNoteReadSerializer(BaseReadSerializer):

    class Meta(BaseReadSerializer.Meta):
        model = TeacherNote


class TeacherProfileReadSerializer(BaseReadSerializer):
    teacher = TeacherReadSerializer()

    class Meta(BaseReadSerializer.Meta):
        model = TeacherProfile
