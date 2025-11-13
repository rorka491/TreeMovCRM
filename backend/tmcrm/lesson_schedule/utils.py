from datetime import time, timedelta, datetime
from typing import Type, TYPE_CHECKING
from typing import List
import json
from collections import defaultdict
from rest_framework.response import Response
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .models import Attendance, Lesson

    

if TYPE_CHECKING:
    from mainapp.models import Organization


def _grouped_response(self, field_name=None, serializer_class=None):
    schedules = self.get_queryset().exclude(**{f"{field_name}__isnull": True})
    filterset = self.filterset_class(self.request.GET, queryset=schedules)
    schedules = filterset.qs

    grouped = defaultdict(list)
    for schedule in schedules:
        key = getattr(schedule, field_name)
        grouped[key].append(schedule)

    response_data = []
    for key_obj, schedule_list in grouped.items():
        serializer = serializer_class(
            instance={f"{field_name}": key_obj, "schedules": schedule_list}
        )
        response_data.append(serializer.data)

    return Response(response_data)


# Создает таску
def init_task_create_update_complete_lessons_task():
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1, period=IntervalSchedule.MINUTES
    )

    PeriodicTask.objects.update_or_create(
        name="Задача обновление статуса урока если он завершен по времени",
        defaults={
            "interval": schedule,
            "task": "lesson_schedule.tasks.update_complete_lessons",
            "args": json.dumps([]),
            "kwargs": json.dumps({}),
        },
    )

def init_task_create_attendences_for_all_passes():
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1, period=IntervalSchedule.MINUTES
    )

    PeriodicTask.objects.update_or_create(
        name="Задача создание записей о пропусках учеников не отмеченных как присутствующих",
        defaults={
            "interval": schedule,
            "task": "lesson_schedule.tasks.create_attendences_for_all_passes",
            "args": json.dumps([]),
            "kwargs": json.dumps({}),
        },
    )




class LessonSlot:
    def __init__(
        self, start_time: time, end_time: time, break_duration: timedelta = timedelta(0)
    ):
        if not self._validate_time(start_time, end_time):
            raise ValueError("Некорректное время урока")
        self.start_time = start_time
        self.end_time = end_time
        self.break_duration = break_duration

    @property
    def break_end_time(self) -> time:
        """Вычисляемое время окончания перерыва"""
        end_dt = datetime.combine(datetime.today(), self.end_time)
        break_end_dt = end_dt + self.break_duration
        return break_end_dt.time()

    @property
    def duration(self) -> timedelta:
        """Длительность урока"""
        return self._time_to_timedelta(self.end_time) - self._time_to_timedelta(
            self.start_time
        )

    def _time_to_timedelta(self, t: time) -> timedelta:
        """Конвертирует time в timedelta"""
        return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

    def _validate_time(self, start: time, end: time) -> bool:
        """Проверяет корректность временного интервала"""
        return start < end

    def is_overlap(self, other: "LessonSlot") -> bool:
        """Проверяет пересечение с другим уроком"""
        self_start = self._time_to_timedelta(self.start_time)
        self_end = self._time_to_timedelta(self.break_end_time)
        other_start = self._time_to_timedelta(other.start_time)
        other_end = self._time_to_timedelta(other.break_end_time)

        return not (self_end <= other_start or other_end <= self_start)

    @staticmethod
    def find_free_slots_at_day(
        lessons: List["LessonSlot"],
        day_start: time = time(6, 0),
        day_end: time = time(23, 0),
    ) -> List[tuple[time, time]]:
        if not lessons:
            return [(day_start, day_end)]

        # Сортируем уроки по времени начала
        sorted_lessons = sorted(lessons, key=lambda x: x.start_time)
        free_slots = []

        # Проверяем интервал до первого урока
        first_lesson = sorted_lessons[0]
        if day_start < first_lesson.start_time:
            free_slots.append((day_start, first_lesson.start_time))

        # Проверяем интервалы между уроками
        for i in range(len(sorted_lessons) - 1):
            current_end = sorted_lessons[i].break_end_time
            next_start = sorted_lessons[i + 1].start_time
            if current_end < next_start:
                free_slots.append((current_end, next_start))

        # Проверяем интервал после последнего урока
        last_lesson = sorted_lessons[-1]
        if last_lesson.break_end_time < day_end:
            free_slots.append((last_lesson.break_end_time, day_end))

        return free_slots

    @classmethod
    def can_add_lesson(
        cls, existing_lessons: List["LessonSlot"], new_lesson: "LessonSlot"
    ) -> bool:

        return all(not new_lesson.is_overlap(lesson) for lesson in existing_lessons)

    def __str__(self):
        return (
            f"Урок: {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')} "
            f"(Перерыв {str(self.break_duration)} до {self.break_end_time.strftime('%H:%M')})"
        )


def _create_missing_attendances_for_lesson(lesson: Lesson) -> list[Attendance]:
    org = lesson.get_org
    group_students = lesson.group.students.all()
    lesson_date = lesson.date
    existing_students_ids = Attendance.objects.filter(lesson=lesson).values_list(
        "student_id", flat=True
    )
    missing_students = group_students.exclude(id__in=existing_students_ids)

    return [
        Attendance(student=student, lesson=lesson, org=org, was_present=False, lesson_date=lesson_date)
        for student in missing_students
    ]


def _get_complited_lessons_for_org(org: "Organization") -> list[Lesson]:
    return Lesson.objects.filter_by_org(org).filter(
        is_canceled=False, is_completed=True
    )


