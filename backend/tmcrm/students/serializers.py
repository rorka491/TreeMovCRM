from rest_framework import serializers
from mainapp.serializers import BaseSerializerExcludeFields
from .models import *
from schedule.models import Attendance


class StudentGroupSerializer(BaseSerializerExcludeFields):

    class Meta:
        model = StudentGroup
        exclude = ['org', 'id']

class AttendanceSerializer(BaseSerializerExcludeFields):

    class Meta:
        model = Attendance
        exclude = ['org, id']
