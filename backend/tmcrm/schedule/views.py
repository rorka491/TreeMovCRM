from rest_framework.decorators import action
from .models import Schedule, Subject
from .serializers import *
from rest_framework.response import Response
from mainapp.views import BaseViewSetWithOrdByOrg, SelectRelatedViewSet, base_search
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from .utils import _grouped_response
from django.db.models import Q

#filters 
class ScheduleFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Schedule
        fields = '__all__'
        

#views
class ScheduleViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
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
    
    @action(detail=False, methods=['post'], url_path='search')
    @base_search
    def search(self, request, query=None):
        words = query.split()
        q = Q()

        for word in words:
            q |= (Q(title__icontains=word) |
                Q(start_time__icontains=word) |
                Q(end_time__icontains=word) |
                Q(date__icontains=word) |
                Q(teacher__employer__name__icontains=word) |
                Q(teacher__employer__surname__icontains=word) |
                Q(teacher__employer__patronymic__icontains=word) |
                Q(classroom__title__icontains=word) |
                Q(classroom__floor__icontains=word) |
                Q(classroom__building__icontains=word) |
                Q(group__name__icontains=word) |
                Q(subject__name__icontains=word))

        results = self.get_queryset().filter(q)
        serializer = self.serializer_class(results, many=True)
        return Response(serializer.data)


class SubjectViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend]

    
class ClassroomViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    filter_backends = [DjangoFilterBackend]

class GradeViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    filter_backends = [DjangoFilterBackend]


class AttendanceViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend]




    