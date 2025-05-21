from django.shortcuts import render
from rest_framework import viewsets
from .models import Employer
from .serializers import EmployerSerializer

class EmployerViewSet(viewsets.ModelViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer