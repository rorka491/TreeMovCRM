from rest_framework import serializers
from mainapp.serializers import BaseSerializerExcludeFields, BaseSerializerWithoutOrg
from .models import *
from employers.serializers import TeacherSerializer
from students.serializers import StudentGroupSerializer 

class ClassroomSerializer(BaseSerializerExcludeFields):

    class Meta:
        model = Classroom
        exclude = ['id', 'org']

class SubjectSerializer(BaseSerializerExcludeFields):

    class Meta:
        model = Subject
        exclude = ['id', 'org']

class GradeSerializer(BaseSerializerExcludeFields):
     
    class Meta:
        model = Grade
        exclude =  ['id', 'org']

class AttendanceSerializer(BaseSerializerExcludeFields):

    class Meta:
        model = Attendance
        exclude =  ['id', 'org']


class ScheduleSerializer(BaseSerializerExcludeFields):
    teacher = TeacherSerializer()
    subject = SubjectSerializer()
    group = StudentGroupSerializer()

    org = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    classroom = ClassroomSerializer()


    class Meta:
        model = Schedule
        fields = '__all__'




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
    




"""Группированые сериализаторы с исключенными полями"""

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




