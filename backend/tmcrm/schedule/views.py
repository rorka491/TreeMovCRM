from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets
from .models import Schedule
from .serializers import ScheduleSerializer, TeacherScheduleSerializer, GroupScheduleSerializer, ClassroomScheduleSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from mainapp.views import BaseViewSetWithOrdByOrg, SelectRelatedViewSet
from collections import defaultdict
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from types import SimpleNamespace
from .utils import _grouped_response

#filters 
class ScheduleFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Schedule
        fields = '__all__'
        

#views
class ScheduleViewSet(BaseViewSetWithOrdByOrg, SelectRelatedViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ScheduleFilter

    select_related_fields = [
        'teacher',
        'teacher__employer',
        'subject',
        'group',
        'org',
        'classroom',
    ]

    
    grouped_fields = {
        'by-teachers': ('teacher', TeacherScheduleSerializer),
        'by-groups': ('group', GroupScheduleSerializer),
        'by-classrooms': ('classroom', ClassroomScheduleSerializer),
    }

    def _grouped_action(self, key):
        field_name, serializer = self.grouped_fields[key]
        return _grouped_response(self, field_name, serializer)

    @action(detail=False, methods=['get'], url_path='by-teachers')
    def by_teachers(self, request):
        return self._grouped_action('by-teachers')

    @action(detail=False, methods=['get'], url_path='by-groups')
    def by_groups(self, request):
        return self._grouped_action('by-groups')

    @action(detail=False, methods=['get'], url_path='by-classrooms')
    def by_classrooms(self, request):
        return self._grouped_action('by-classrooms')
    
