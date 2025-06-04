from rest_framework import serializers
from mainapp.serializers import BaseSerializerExcludeFields, BaseSerilizeWithOutOrg
from .models import *
from employers.serializers import TeacherSerializer
from students.serializers import GroupSerializer 

class ClassroomSerializer(BaseSerializerExcludeFields):

    class Meta:
        model = Classroom
        exclude = ['org', 'id']

class ScheduleSerializer(BaseSerializerExcludeFields):
    teacher = TeacherSerializer()
    subject = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    group = GroupSerializer()

    org = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    classroom = ClassroomSerializer()


    class Meta:
        model = Schedule
        fields = '__all__'


class ScheduleGroupSerializer(serializers.Serializer):
    schedules = serializers.SerializerMethodField()
    exclude_fields = []

    def get_schedules(self, obj):
        print(f'класс obj {type(obj)}')
        schedules_qs = obj['schedules']
        return ScheduleSerializer(
            schedules_qs,
            many=True,
            exclude_fields = self.exclude_fields
        ).data 

class TeacherScheduleSerializer(ScheduleGroupSerializer):
    teacher = TeacherSerializer()
    exclude_fields = ['teacher']

    class Meta: 
        fields = ['teacher', 'schedules']

class ClassroomScheduleSerializer(ScheduleGroupSerializer):
    classroom = ClassroomSerializer()
    exclude_fields = ['classroom']

    class Meta: 
        fields = ['classroom', 'schedules']

class GroupScheduleSerializer(ScheduleGroupSerializer):
    group = GroupSerializer(exclude_fields=['students'])
    exclude_fields = ['group']

    class Meta: 
        fields = ['group', 'schedules']




