from rest_framework import serializers
from mainapp.serializers import BaseSerializerExcludeFields
from .models import Teacher, Employer, Documents, DocumentsTypes


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['name', 'surname', 'patronymic']

class TeacherSerializer(BaseSerializerExcludeFields):
    employer = EmployerSerializer(read_only=True) 

    class Meta:
        model = Teacher
        fields = ['employer']


class DocumentsTypesSerializer(BaseSerializerExcludeFields):

    class Meta:
        model = DocumentsTypes
        fields = '__all__'

class DocumentsSerializer(BaseSerializerExcludeFields):
    employer = EmployerSerializer(read_only=True)
    doc_type = DocumentsTypesSerializer(read_only=True)

    class Meta:
        model = Documents
        fields = '__all__'