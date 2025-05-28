from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend  


class ScheduleViewSet(viewsets.ModelViewSet):  
    queryset = Schedule.objects.all()  
    serializer_class = ScheduleSerializer  

    def get_queryset(self):  
        queryset = super().get_queryset()  
        teacher_id = self.request.query_params.get('teacher')  
        group_id = self.request.query_params.get('group')  
        date = self.request.query_params.get('date')  

        if teacher_id:  
            queryset = queryset.filter(teacher_id=teacher_id)  
        if group_id:  
            queryset = queryset.filter(group_id=group_id)  
        if date:  
            queryset = queryset.filter(date=date)  

        return queryset  



class SubjectViewSet(viewsets.ModelViewSet):  
    queryset = Subject.objects.all()  
    serializer_class = SubjectSerializer 


class AttendanceViewSet(viewsets.ModelViewSet):  
    queryset = Attendance.objects.all()  
    serializer_class = AttendanceSerializer 


class GradeViewSet(viewsets.ModelViewSet):  
    queryset = Grade.objects.all()  
    serializer_class = GradeSerializer 





