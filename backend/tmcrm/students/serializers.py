from rest_framework import serializers
from mainapp.serializers import BaseSerializerExcludeFields
from .models import *
from schedule.models import Attendance



class AttendanceSerializer(BaseSerializerExcludeFields):

    class Meta(BaseSerializerExcludeFields.Meta):
        model = Attendance
        exclude = ['org, id']

class StudentSerializer(BaseSerializerExcludeFields):

    class Meta(BaseSerializerExcludeFields.Meta):
        model = Student

class StudentGroupSerializer(BaseSerializerExcludeFields):
    students = StudentSerializer(many=True)

    class Meta(BaseSerializerExcludeFields.Meta):
        model = StudentGroup