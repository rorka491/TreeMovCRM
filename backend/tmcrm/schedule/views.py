from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets
from .models import Schedule
from .serializers import ScheduleSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from mainapp.views import BaseViewSetWithOrdByOrg
from collections import defaultdict


class ScheduleViewSet(BaseViewSetWithOrdByOrg):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    grouped_fields = {
        'by-teachers': 'teacher_id',
        'by-groups': 'group_id',
        'by-classrooms': 'classroom',
    }

    def _grouped_response(self, field_name):
        schedules = self.get_queryset().exclude(**{field_name + '__isnull': True})
        grouped = defaultdict(list)

        for schedule in schedules:
            key = getattr(schedule, field_name)
            grouped[key].append(schedule)

        response_data = []
        for key, schedule_list in grouped.items():
            serialized = self.get_serializer(schedule_list, many=True)
            response_data.append({
                field_name: key,
                'schedules': serialized.data
            })
        return Response(response_data)

    @action(detail=False, methods=['get'], url_path='by-teachers')
    def by_teachers(self, request):
        return self._grouped_response(self.grouped_fields['by-teachers'])

    @action(detail=False, methods=['get'], url_path='by-groups')
    def by_groups(self, request):
        return self._grouped_response(self.grouped_fields['by-groups'])

    @action(detail=False, methods=['get'], url_path='by-classrooms')
    def by_classrooms(self, request):
        return self._grouped_response(self.grouped_fields['by-classrooms'])
    
        

class WomenAPIView(APIView):

    def get(self, request):
        return Response({'title': 'Angelina Jolie'})

"""
class SubjectViewSet(viewsets.ModelViewSet):  
    queryset = Subject.objects.all()  
    serializer_class = SubjectSerializer 


class AttendanceViewSet(viewsets.ModelViewSet):  
    queryset = Attendance.objects.all()  
    serializer_class = AttendanceSerializer 


class GradeViewSet(viewsets.ModelViewSet):  
    queryset = Grade.objects.all()  
    serializer_class = GradeSerializer 
"""
'''
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





'''





        


    
     
    



