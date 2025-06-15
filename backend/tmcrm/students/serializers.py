from rest_framework import serializers
from mainapp.serializers import BaseSerializerExcludeFields
from .models import *
from schedule.models import Attendance



class AttendanceSerializer(BaseSerializerExcludeFields):

    class Meta(BaseSerializerExcludeFields.Meta):
        model = Attendance
        exclude = ['org, id']



class StudentGroupSerializer(BaseSerializerExcludeFields):

    class Meta(BaseSerializerExcludeFields.Meta):
        model = StudentGroup

class StudentSerializer(BaseSerializerExcludeFields):
    groups = StudentGroupSerializer(exclude_fields=['students'])

    class Meta(BaseSerializerExcludeFields.Meta):
        model = Student