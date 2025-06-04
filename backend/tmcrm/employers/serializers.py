from rest_framework import serializers
from mainapp.serializers import BaseSerializerExcludeFields
from .models import Teacher, Employer


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['name', 'surname', 'patronymic']

class TeacherSerializer(BaseSerializerExcludeFields):
    employer = EmployerSerializer(read_only=True) 

    class Meta:
        model = Teacher
        fields = ['employer']



# class TeacherScheduleSerializer(serializers.Serializer):
#     teacher = EmployerSerializer()
#     schedules = ScheduleSerializer(many=True)

