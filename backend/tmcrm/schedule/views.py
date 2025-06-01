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
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        filters = request.query_params.dict()
        print(filters)
        schedules = Schedule.objects.filter(**filters)
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)


        

    
        

    
     
    



