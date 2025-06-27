from rest_framework import serializers
from mainapp.serializers import BaseSerializerExcludeFields, ColorSerializer
from .models import *
from employers.serializers import TeacherSerializer
from students.serializers import StudentGroupSerializer, StudentSerializer
  
class ClassroomSerializer(BaseSerializerExcludeFields):

    class Meta(BaseSerializerExcludeFields.Meta):
        model = Classroom

class SubjectSerializer(BaseSerializerExcludeFields):
    color = ColorSerializer()

    class Meta(BaseSerializerExcludeFields.Meta):
        model = Subject

class AttendanceSerializer(BaseSerializerExcludeFields):

    class Meta:
        model = Attendance

class ScheduleSerializer(BaseSerializerExcludeFields):
    teacher = TeacherSerializer()
    subject = SubjectSerializer(exclude_fields=['teacher'])
    group = StudentGroupSerializer(exclude_fields=['students'])
    classroom = ClassroomSerializer()


    class Meta(BaseSerializerExcludeFields.Meta):
        model = Schedule

class PeriodScheduleSerializer(BaseSerializerExcludeFields):
    teacher = TeacherSerializer()
    subject = SubjectSerializer()
    group = StudentGroupSerializer(exclude_fields=['students'])
    classroom = ClassroomSerializer()

    class Meta(BaseSerializerExcludeFields.Meta):
        model = PeriodSchedule


"""Группированые сериализаторы с исключенными полями"""

class ScheduleStudentGroupSerializer(serializers.Serializer):
    schedules = serializers.SerializerMethodField()
    exclude_fields = []

    def get_schedules(self, obj):
        schedules_qs = obj['schedules']
        return ScheduleSerializer(
            schedules_qs,
            many=True,
            exclude_fields = self.exclude_fields
        ).data 

class TeacherScheduleSerializer(ScheduleStudentGroupSerializer):
    """"""
    teacher = TeacherSerializer()
    exclude_fields = ['teacher']

    class Meta: 
        fields = ['teacher', 'schedules']

class ClassroomScheduleSerializer(ScheduleStudentGroupSerializer):
    """"""
    classroom = ClassroomSerializer()
    exclude_fields = ['classroom']

    class Meta: 
        fields = ['classroom', 'schedules']

class GroupScheduleSerializer(ScheduleStudentGroupSerializer):
    """"""
    group = StudentGroupSerializer(exclude_fields=['students'])
    exclude_fields = ['group']

    class Meta: 
        fields = ['group', 'schedules']

"""_________________________________________________"""


class GradeSerializer(BaseSerializerExcludeFields):
    student = StudentSerializer()
    lesson = ScheduleSerializer(
        un_exclude_fields=['subject', 'date', 'teacher', 'group'])


    class Meta(BaseSerializerExcludeFields.Meta):
        model = Grade
        exclude =  ['org', 'created_at', 'updated_at']

