from rest_framework import serializers
from .models import Teacher, Employer

class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['name', 'surname', 'patronymic', 'birthday']

class TeacherSerializer(serializers.ModelSerializer):
    employer = EmployerSerializer(read_only=True) 

    class Meta:
        model = Teacher
        fields = ['employer']