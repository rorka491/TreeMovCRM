from rest_framework.decorators import action
from rest_framework.response import Response
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from mainapp.views import BaseViewSetWithOrdByOrg, SelectRelatedViewSet, base_search
from .utils import _grouped_response
from .serializers import (
    AttendanceSerializer,
    ClassroomScheduleSerializer,
    ClassroomSerializer,
    PeriodScheduleSerializer,
    ScheduleSerializer,
    SubjectSerializer,
    TeacherScheduleSerializer,
    GroupScheduleSerializer,
    GradeSerializer,
)
from .models import Attendance, Schedule, Subject, PeriodSchedule, Grade, Classroom
from .mixins import SerializerUpdateMixin, LessonValidationMixin


# filters
class ScheduleFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Schedule
        fields = "__all__"


class GradeFilter(django_filters.FilterSet):

    class Meta:
        model = Grade
        fields = "__all__"


# views
class ScheduleViewSet(
    SelectRelatedViewSet,
    BaseViewSetWithOrdByOrg,
    SerializerUpdateMixin,
    LessonValidationMixin,
):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ScheduleFilter

    critical_fields = (
        "classroom",
        "teacher",
        "date",
        "group",
        "start_time",
        "end_time",
    )

    select_related_fields = [
        "teacher",
        "teacher__employer",
        "subject",
        "group",
        "org",
        "classroom",
    ]

    grouped_fields = {
        "by-teachers": ("teacher", TeacherScheduleSerializer),
        "by-groups": ("group", GroupScheduleSerializer),
        "by-classrooms": ("classroom", ClassroomScheduleSerializer),
    }

    def update(self, request, *args, **kwargs):
        is_force_update = request.query_params.get("is_force_update")

        data = request.data
        partial = kwargs.get("partial", False)
        instance = self.get_object()
        serializer = self.get_update_serializer(instance, data, partial)

        should_check = any(field in data for field in self.critical_fields)

        if not should_check or self.can_update_alone_lesson(
            serializer=serializer,
            is_force_update=is_force_update,
        ):
            serializer.save()

        return Response(serializer.data)

    def _grouped_action(self, key):
        field_name, serializer = self.grouped_fields[key]
        return _grouped_response(self, field_name, serializer)

    @action(detail=False, methods=["get"], url_path="by-teachers")
    def by_teachers(self, request):
        return self._grouped_action("by-teachers")

    @action(detail=False, methods=["get"], url_path="by-groups")
    def by_groups(self, request):
        return self._grouped_action("by-groups")

    @action(detail=False, methods=["get"], url_path="by-classrooms")
    def by_classrooms(self, request):
        return self._grouped_action("by-classrooms")

    @action(detail=False, methods=["post"], url_path="search")
    @base_search
    def search(self, request, query=None):
        q = Q()

        for word in query.split():
            q |= (
                Q(title__icontains=word)
                | Q(start_time__icontains=word)
                | Q(end_time__icontains=word)
                | Q(date__icontains=word)
                | Q(teacher__employer__name__icontains=word)
                | Q(teacher__employer__surname__icontains=word)
                | Q(teacher__employer__patronymic__icontains=word)
                | Q(classroom__title__icontains=word)
                | Q(classroom__floor__icontains=word)
                | Q(classroom__building__icontains=word)
                | Q(group__name__icontains=word)
                | Q(subject__name__icontains=word)
            )

        results = self.get_queryset().filter(q)
        serializer = self.serializer_class(results, many=True)
        return Response(serializer.data)


class PeriodScheduleViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg, SerializerUpdateMixin):
    queryset = PeriodSchedule.objects.all()
    serializer_class = PeriodScheduleSerializer
    filter_backends = [DjangoFilterBackend]

    critical_fields = (
        "start_time",
        "end_time",
        "teacher",
        "classroom",
        "group",
    )

    def get_lessons_queryset(self):
        queryset = Schedule.objects.all()
        return self.filter_by_user_org(queryset)
        

    def update(self, request, *args, **kwargs):
        data = request.data
        partial = kwargs.get("partial", False)
        instance = self.get_object()
        serializer = self.get_update_serializer(instance, data, partial)

        should_check = any(field in data for field in self.critical_fields)

        if not should_check or self.can_update_period_lesson(serializer=serializer):
            serializer.save()
        

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
    filterset_class = GradeFilter
    serializer_class = GradeSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):

        queryset = super().get_queryset()
        last = self.request.query_params.get("last")

        if last and last.isdigit():
            return queryset[: int(last)]

        return queryset


class AttendanceViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend]
