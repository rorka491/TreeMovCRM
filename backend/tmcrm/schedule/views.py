from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import ScheduleSerializer
from django_filters.rest_framework import DjangoFilterBackend  


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    

class ScheduleByTeacherViewSet(viewsets.ModelViewSet):  
    queryset = Schedule.objects.all()  
    serializer_class = ScheduleSerializer  
    filter_backends = [DjangoFilterBackend]  
    filterset_fields = ['teacher']