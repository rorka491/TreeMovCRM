from datetime import date
from functools import total_ordering
import re
from typing import TYPE_CHECKING, Dict
from django.db.models import Count, Q, Max, Sum, Min, Avg, F
from rest_framework.response import Response
from rest_framework.decorators import action
from mainapp.exceptions.analisys_exceptions import HasNoStudentsSnapShot
from mainapp.views import (
    SelectRelatedViewSet,
    BaseViewSetWithOrdByOrg,
    RequiredQueryParamsMixin,
    SelectrealtedByModelsViewSet
)
from mainapp.permissions import OrgParamsPermission
from lesson_schedule.models import Attendance, Grade, Schedule
from lesson_schedule.serializers.read import ScheduleReadSerializer
from employers.models import Employer, Teacher
from students.models import Student, StudentsSnapshot, StudentGroup
from .utils import (
    _calculate_attendances_rate,
    _calcutate_student_success_rate,
    format_duration,
)
from .filters import AttendanceFilter, StudentSnapshotFilter, GradeFilter, LessonFilter, StudentFilter
from mainapp.exceptions.user_exceptions import UserHasNoOrg


if TYPE_CHECKING:
    from django.db.models import QuerySet


# views


class BaseMetricsViewSet(
    SelectrealtedByModelsViewSet, # класс для оптимизации запросов вьюстеа без своего queryset 
    BaseViewSetWithOrdByOrg, 
    RequiredQueryParamsMixin
):
    queryset = None        

    prefetch_related_fields_by_model = {
        "StudentGroup": ("students",),
        }

    select_related_fields_by_model = {
        "Attendance": (
            "student",
            "lesson",
        ),
        "Grade": (
            "student",
            "lesson",
        ),
        "Schedule": (
            "classroom",
            "teacher",
            "group",
            "subject",
            "period_schedule",
        ),
    }

    # Запросы оптимизированы
    def _get_student_group_queryset(self) -> "QuerySet[StudentGroup]":
        return self.optimize_queryset(queryset=StudentGroup.org_objects.all())

    def _get_attendance_queryset(self) -> "QuerySet[Attendance]":
        return self.optimize_queryset(queryset=Attendance.org_objects.all())

    def _get_grade_queryset(self) -> "QuerySet[Grade]":
        return self.optimize_queryset(queryset=Grade.org_objects.all())

    def _get_students_queryset(self) -> "QuerySet[Student]":
        return Student.org_objects.all()

    def _get_student_snapshot(self) -> "QuerySet[StudentsSnapshot]":
        return StudentsSnapshot.org_objects.all()

    def _get_lessons_queryset(self) -> "QuerySet[Schedule]":
        return self.optimize_queryset(queryset=Schedule.org_objects.all())


class MetricsViewSet(BaseMetricsViewSet):
    """
    Класс возвращает разные метрические показатели в разных типах данных
    """

    queryset = None

    def get_permissions(self):
        perms = super().get_permissions()
        match self.action:
            case "get_worked_hours":
                perms.append(
                    OrgParamsPermission({"teacher": Teacher, "group": StudentGroup})
                )

        return perms 

    def _get_groups_count(self, queryset: "QuerySet[StudentGroup]") -> dict[str, int]:     
        count = queryset.count()
        return {"groups_count": count} 

    def _get_employee_count(self, queryset: "QuerySet[Employer]") -> dict[str, int]:
        count = queryset.count()
        return {"employee_count": count}

    def _get_students_count(self, queryset: "QuerySet[Student]") -> dict[str, int]:
        count = queryset.count()
        return {"students_count": count}

    def _aggregate_attendences(self, queryset) -> Dict[str, int]:
        aggregate_data = queryset.aggregate(
            total=Count("id"),
            presents=Count("id", filter=Q(was_present=True)),
            start_date=Min("lesson_date"),
            end_date=Max("lesson_date"),
        )
        total = aggregate_data["total"] or 0
        presents = aggregate_data["presents"] or 0
        aggregate_data["rate"] = _calculate_attendances_rate(presents, total)
        return aggregate_data

    def _aggregate_student_success_rate(self, queryset) -> Dict[str, int]:
        aggregate_data = queryset.aggregate(
            total_quantity_grades=Count("id"),
            sum_grades=Sum("value"),
            start_date=Min("grade_date"),
            end_date=Max("grade_date"),
        )            
        total_quantity_grades = aggregate_data["total_quantity_grades"] or 0
        sum_grades = aggregate_data["sum_grades"] or 0
        aggregate_data["rate"] = _calcutate_student_success_rate(
            total_quantity_grades, sum_grades
        )
        return aggregate_data

    def _aggregate_worked_time(self, queryset):
        """Время получается в секундах"""
        result = queryset.aggregate(total_seconds=Sum('duration'))
        total_seconds = result["total_seconds"]
        return total_seconds

    @action(detail=False, methods=["get"], url_path="attendance")
    def get_attendances_rate(self, request):
        queryset = AttendanceFilter(
            request.GET, queryset=self._get_attendance_queryset()
        ).qs      

        agg= self._aggregate_attendences(queryset)
        return Response(agg)

    @action(detail=False, methods=["get"], url_path="grade")
    def get_student_success_rate(self, request):
        queryset = GradeFilter(
            request.GET, queryset=self._get_grade_queryset()
        ).qs

        agg = self._aggregate_student_success_rate(queryset)
        return Response(agg)              

    @action(detail=False, methods=["get"], url_path="student_snapshot")
    def get_student_snapshot(self, request):
        error_resp = self.validate_required_query_params(request, ["date"])
        if error_resp:
            return error_resp

        queryset = StudentSnapshotFilter(
            request.GET, queryset=self._get_student_snapshot()
        ).qs.first()

        if not queryset:
            raise HasNoStudentsSnapShot

        total_clients = queryset.total_clients
        date = queryset.date

        return Response({"total_clients": total_clients, "date": date})

    @action(
        detail=False,
        methods=["get"],
        url_path="worked_hours",
    )
    def get_worked_hours(self, request):
        queryset = LessonFilter(request.GET, queryset=self._get_lessons_queryset()).qs
        serializer = ScheduleReadSerializer(
            queryset, many=True, exclude_fields=["teacher", "subject", "classroom"]
        )
        worked_seconds = self._aggregate_worked_time(queryset)
        worked_hours = format_duration(worked_seconds)

        return Response({"worked_hours": worked_hours, "lessons": serializer.data})

    @action(
        detail=False,
        methods=['get'],
        url_path='groups_count'
    )
    def get_groups_count(self, request):
        queryset= self._get_student_group_queryset()
        data = self._get_groups_count(queryset)
        return Response(data)

    @action(
        detail=False,
        methods=['get'],
        url_path='students_count'
    )
    def get_students_count(self, request):
        queryset = StudentFilter(request.GET, queryset=self._get_students_queryset()).qs
        data = self._get_students_count(queryset)
        return Response(data)


class AnalyticsChartsViewSet(BaseMetricsViewSet):
    queryset = None

    def _get_average_grade_by_date(self, queryset: "QuerySet[Grade]"):
        return queryset.values("grade_date").annotate(avg_grade=Avg("value")).order_by("grade_date")

    def _get_clients_by_date(self, queryset: "QuerySet[StudentsSnapshot]"):
        return queryset.values("date", "total_clients").order_by("date")

    def _get_attendance_by_date(self, queryset: "QuerySet[Attendance]"):
        return queryset.values("lesson_date").annotate(
            total=Count("id"), presents=Count("id", filter=Q(was_present=True))
        )   

    def _get_worked_hours_by_date(self, queryset: "QuerySet[Schedule]"):
        return queryset.values('date').annotate(total_hours=Sum(F('duration')))

    @action(
        detail=False,
        methods=["get"],
        url_path="grades"
    )
    def get_grades_chart(self, request) -> Response: 
        queryset = GradeFilter(request.GET, queryset=self._get_grade_queryset()).qs
        data = self._get_average_grade_by_date(queryset)
        return Response(list(data))           

    @action(
        detail=False,
        methods=['get'],
        url_path='clients_dynamic'
    )
    def get_clients_chart(self, request):
        queryset = StudentSnapshotFilter(request.GET, queryset=self._get_student_snapshot()).qs
        data = self._get_clients_by_date(queryset)
        return Response(data)

    @action(
        detail=False,
        methods=["get"],
        url_path="attendance"
    )
    def get_attendance_chart(self, request):
        queryset = AttendanceFilter(request.GET, queryset=self._get_attendance_queryset()).qs 
        data = self._get_attendance_by_date(queryset)
        return Response(data)

    @action(
        detail=False,
        methods=['get'],
        url_path='worked_hours'
    )                          
    def get_worked_hours_by_date(self, request):
        queryset = LessonFilter(request.GET, queryset=Schedule.org_objects.all()).qs
        data = self._get_worked_hours_by_date(queryset)
        return Response(data)
