'''
from rest_framework import serializers
from .models import *
from employers.models import *
from students.models import *  
from schedule.models import Subject
from employers.serializers import *
'''
from rest_framework import serializers
from .models import *
from employers.serializers import TeacherSerializer


class ScheduleSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()  

    class Meta:
        model = Schedule
        fields = '__all__'


'''
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__' # ('id', 'title', 'start_time', 'end_time', 'date', 'teacher') 


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

'''