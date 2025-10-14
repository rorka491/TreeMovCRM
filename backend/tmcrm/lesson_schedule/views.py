from typing import Tuple
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
import django_filters
from django.db.models import Q

from .filters import LessonFilter
from .serializers.read import AttendanceReadSerializer, ClassroomReadSerializer, GradeReadSerializer, ScheduleReadSerializer, SubjectReadSerializer, PeriodScheduleReadSerializer
from .serializers.write import AttendanceWriteSerializer, ClassroomWriteSerializer, GradeWriteSerializer, PeriodScheduleWriteSerializer, ScheduleWriteSerializer, SubjectWriteSerializer
from mainapp.views import BaseViewSetWithOrdByOrg, SelectRelatedViewSet, base_search
from mainapp.filters import DateRangeMixin
from .utils import _grouped_response
from .models import Attendance, Schedule, Subject, PeriodSchedule, Grade, Classroom
from .mixins import SerializerUpdateMixin, LessonValidationMixin
from .serializers.other import GroupScheduleSerializer, TeacherScheduleSerializer, ClassroomScheduleSerializer


# filters
class ScheduleFilter(DateRangeMixin, django_filters.FilterSet):

    class Meta:
        model = Schedule
        exclude = ["duration"]


class GradeFilter(django_filters.FilterSet):

    class Meta:
        model = Grade
        fields = "__all__"


# views
class AbstractScheduleViewSet(
    SelectRelatedViewSet,
    BaseViewSetWithOrdByOrg,
    SerializerUpdateMixin,
    LessonValidationMixin,
):
    """
    Класс объединяет в себе методы и атрибуты классов
    ScheduleViewSet и PeriodScheduleViewSet для избежания дублирования
    """
    abstract = True
    critical_fields: Tuple[str, ...] = ()

    def _has_critical_fields(self, data: dict) -> bool:
        return any(field in data for field in self.critical_fields)

    def _can_update(self, serializer, is_force_update) -> bool:
        raise NotImplementedError("Метод не был реализован в наслдениках")

    def get_lessons_queryset(self):
        queryset = Schedule.objects.all()
        return queryset

    def update(self, request, *args, **kwargs):
        is_force_update = request.query_params.get("is_force_update")
        data = request.data
        partial = kwargs.get("partial", False) # Если false то запрос PUT в обратном случае PATCH
        instance = self.get_object()
        serializer = self.get_update_serializer(instance, data, partial)

        if not self._has_critical_fields(data) or self._can_update(
            serializer=serializer,
            is_force_update=is_force_update,
        ):
            serializer.save()
            return Response(serializer.data)

        raise ValidationError({"detail": "Невозможно обновить критичные поля"})


class ScheduleViewSet(AbstractScheduleViewSet):
    queryset = Schedule.objects.all()
    filterset_class = LessonFilter
    read_serializer_class = ScheduleReadSerializer
    write_serializer_class = ScheduleWriteSerializer


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


    def _can_update(self, serializer, is_force_update) -> bool:
        return self.can_update_alone_lesson(
            serializer=serializer, is_force_update=is_force_update
        )

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


class PeriodScheduleViewSet(AbstractScheduleViewSet):
    queryset = PeriodSchedule.objects.all()
    write_serializer_class = PeriodScheduleWriteSerializer
    read_serializer_class = PeriodScheduleReadSerializer

    
    critical_fields = (
        "start_time",
        "end_time",
        "teacher",
        "classroom",
        "group",
    )

    def _can_update(self, serializer, is_force_update) -> bool:
        return self.can_update_period_lesson(serializer=serializer, is_force_update=is_force_update)


class SubjectViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = Subject.objects.all()
    read_serializer_class = SubjectReadSerializer
    write_serializer_class = SubjectWriteSerializer


class ClassroomViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = Classroom.objects.all()
    read_serializer_class = ClassroomReadSerializer
    write_serializer_class = ClassroomWriteSerializer


class GradeViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = Grade.objects.all()
    filterset_class = GradeFilter
    read_serializer_class = GradeReadSerializer
    write_serializer_class = GradeWriteSerializer

    def get_queryset(self):

        queryset = super().get_queryset()
        last = self.request.query_params.get("last")

        if last and last.isdigit():
            return queryset[: int(last)]

        return queryset


class AttendanceViewSet(SelectRelatedViewSet, BaseViewSetWithOrdByOrg):
    queryset = Attendance.objects.all()
    read_serializer_class = AttendanceReadSerializer
    write_serializer_class = AttendanceWriteSerializer

