from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets
from .models import Schedule
from .serializers import ScheduleSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    @action(detail=False, methods=['get'], url_path='by-teachers')
    def by_teachers(self, request):
        schedules = self.queryset.filter(teacher__isnull=False)
        serializer = self.get_serializer(schedules, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-groups')
    def by_groups(self, request):
        schedules = self.queryset.filter(group__isnull=False)
        serializer = self.get_serializer(schedules, many=True)
        return Response(serializer.data)
    
        

class WomenAPIView(APIView):

    def get(self, request):
        return Response({'title': 'Angelina Jolie'})
    
     
    



