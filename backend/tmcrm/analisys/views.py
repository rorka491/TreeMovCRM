from typing import TYPE_CHECKING, Dict
from django.db.models import Count, Q, Sum
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from mainapp.views import (
    SelectRelatedViewSet,
    BaseViewSetWithOrdByOrg,
    RequiredQueryParamsMixin,
)
from mainapp.permissions import OrgParamsPermission
from lesson_schedule.models import Attendance, Grade, Schedule
from lesson_schedule.serializers.read import ScheduleReadSerializer
from employers.models import Teacher
from students.models import Student, StudentsSnapshot, StudentGroup
from .utils import _calculate_attendances_rate, _calcutate_student_success_rate
from .filters import AttendanceFilter, StudentSnapshotFilter, GradeFilter, LessonFilter


if TYPE_CHECKING:
    from django.db.models import QuerySet


# views
class MetricsViewSet(
    SelectRelatedViewSet, BaseViewSetWithOrdByOrg, RequiredQueryParamsMixin
):
    """
    Класс возвращает разные метричиские показатели в разных типах данных
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

    def _get_attendance_queryset(self) -> "QuerySet[Attendance]":
        return Attendance.org_objects.all()

    def _get_grade_queryset(self) -> "QuerySet[Grade]":
        return Grade.org_objects.all()

    def _get_students_queryset(self) -> "QuerySet[Student]":
        return Student.org_objects.all()

    def _get_student_snapshot(self) -> "QuerySet[StudentsSnapshot]":
        return StudentsSnapshot.org_objects.all()

    def _get_lessons_queryset(self):
        return Schedule.org_objects.filter(is_completed=True)

    def _aggregate_attendences(self, queryset) -> Dict[str, int]:
        return queryset.aggregate(
            total=Count("id"), presents=Count("id", filter=Q(was_present=True))
        )

    def _aggregate_student_success_rate(self, queryset) -> Dict[str, int]:
        return queryset.aggregate(
            total_quantity_grades=Count("id"), sum_grades=Sum("value")
        )

    def _aggregate_worked_hours(self, queryset):
        total_hours = 0
        for lesson in queryset:
            if lesson.start_time and lesson.end_time:
                total_hours += lesson.duration_hours
        return total_hours

    @action(detail=False, methods=["get"], url_path="attendance")
    def get_attendances_rate(self, request):
        queryset = AttendanceFilter(
            request.GET, queryset=self._get_attendance_queryset()
        ).qs

        agg = self._aggregate_attendences(queryset)

        total = agg["total"] or 0
        presents = agg["presents"] or 0

        return Response(
            {
                "rate": _calculate_attendances_rate(presents, total),
                "total": total,
                "present": presents,
            }
        )

    @action(detail=False, methods=["get"], url_path="grade")
    def get_student_success_rate(self, request):
        queryset = GradeFilter(request.GET, queryset=self._get_grade_queryset()).qs

        agg = self._aggregate_student_success_rate(queryset)

        total_quantity_grades = agg["total_quantity_grades"]
        sum_grades = agg["sum_grades"]

        return Response(
            {
                "rate": _calcutate_student_success_rate(
                    total_quantity_grades, sum_grades
                ),
                "total_quantity_grades": total_quantity_grades,
                "sum_grades": sum_grades,
            }
        )

    @action(detail=False, methods=["get"], url_path="student_snapshot")
    def get_student_snapshot(self, request):
        error_resp = self.validate_required_params(request, ["date"])
        if error_resp:
            return error_resp

        queryset = StudentSnapshotFilter(
            request.GET, queryset=self._get_student_snapshot()
        ).qs

        if len(queryset) > 1:
            queryset = queryset.first()

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
        worked_hours = self._aggregate_worked_hours(queryset)

        return Response({"worked_hours": worked_hours, "lessons": serializer.data})
