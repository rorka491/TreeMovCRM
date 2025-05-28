from rest_framework import serializers
from .models import Teacher, Employer, JobTitle

class TeacherSerializer(serializers.ModelSerializer):
    # Добавляем поля из связанной модели Employer
    name = serializers.CharField(source='employer.name', read_only=True)
    surname = serializers.CharField(source='employer.surname', read_only=True)
    patronymic = serializers.CharField(source='employer.patronymic', read_only=True)
    
    class Meta:
        model = Teacher
        fields = '__all__'