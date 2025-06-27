from rest_framework import serializers
from mainapp.serializers import BaseSerializerExcludeFields
from .models import *
from lesson_schedule.models import Attendance



class AttendanceSerializer(BaseSerializerExcludeFields):

    class Meta(BaseSerializerExcludeFields.Meta):
        model = Attendance
        exclude = ['org, id']


class StudentGroupSerializer(BaseSerializerExcludeFields):

    class Meta(BaseSerializerExcludeFields.Meta):
        model = StudentGroup

class StudentSerializer(BaseSerializerExcludeFields):
    groups = StudentGroupSerializer(many=True, read_only=True, exclude_fields=['students', 'org'])

    class Meta(BaseSerializerExcludeFields.Meta):
        model = Student

class ParentSerializer(BaseSerializerExcludeFields):
    child = StudentSerializer(many=True, read_only=True, exclude_fields=[])

    class Meta(BaseSerializerExcludeFields.Meta):
        model = Parent 
