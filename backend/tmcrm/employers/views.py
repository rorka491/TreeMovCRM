from django.shortcuts import render
from employers.serializers import TeacherSerializer, EmployerSerializer
from mainapp.views import BaseViewSetWithOrdByOrg
from .models import Teacher, Employer

class TeacherViewset(BaseViewSetWithOrdByOrg):
    queryset = Teacher.objects.select_related('employer').all()
    serializer_class = TeacherSerializer

class EmployerViewSet(BaseViewSetWithOrdByOrg):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer





