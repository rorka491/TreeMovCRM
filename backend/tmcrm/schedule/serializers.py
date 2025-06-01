from rest_framework import serializers
from .models import *
from employers.serializers import TeacherSerializer


class ScheduleSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()  

    class Meta:
        model = Schedule
        fields = '__all__'


