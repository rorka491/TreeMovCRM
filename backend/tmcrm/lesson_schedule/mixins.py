from __future__ import annotations
from django.db.models import Q
from django.core.exceptions import ValidationError
from mainapp.serializers import BaseSerializerExcludeFields
from lesson_schedule.utils import LessonSlot


class SerializerUpdateMixin:
    """Миксин для сокрщения стандартной процедуры валидации сериализатора"""

    def get_update_serializer(
        self, instance, data, partial=False
    ) -> BaseSerializerExcludeFields:
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        return serializer

class LessonValidationMixin:
    """Микисин модернизирующий """

    def can_update_alone_lesson_by_fields(
    self,
    instance,
    *,
    start_time,
    end_time,
    date,
    teacher,
    classroom,
    group,
    ):
        all_lessons_at_day = (
            self.get_queryset()
            .filter(date=date)
            .filter(Q(teacher=teacher) | Q(classroom=classroom) | Q(group=group))
            .exclude(pk=instance.pk)
        )

        lesson_list = [
            LessonSlot(lesson.start_time, lesson.end_time) for lesson in all_lessons_at_day
        ]
        current_lesson = LessonSlot(start_time, end_time)

        if LessonSlot.can_add_lesson(lesson_list, current_lesson):
            return True
        else:
            slots = LessonSlot.find_free_slots_at_day(lesson_list)
            raise ValidationError(
                {
                    "detail": "Невозможно обновить время урока на заданное время",
                    "free_slots": slots,
                    "lesson_list": lesson_list,
                    "current_date": date,
                }
            )

    def can_update_alone_lesson(
        self,
        serializer: BaseSerializerExcludeFields,
        is_force_update=False,
    ):
        if is_force_update:
            return True

        instance = serializer.instance
        new_data = serializer.validated_data

        return self.can_update_alone_lesson_by_fields(
            instance,
            start_time=new_data.get("start_time", instance.start_time),
            end_time=new_data.get("end_time", instance.end_time),
            date=new_data.get("date", instance.date),
            teacher=new_data.get("teacher", instance.teacher),
            classroom=new_data.get("classroom", instance.classroom),
            group=new_data.get("group", instance.group),
        )

    def can_update_period_lesson(
        self, serializer: BaseSerializerExcludeFields, is_force_update=False
    ):
        if is_force_update:
            return True

        instance = serializer.instance
        new_data = serializer.validated_data

        start_time = new_data.get("start_time", instance.start_time)
        end_time = new_data.get("end_time", instance.end_time)
        teacher = new_data.get("teacher", instance.teacher)
        classroom = new_data.get("classroom", instance.classroom)
        group = new_data.get("group", instance.group)

        all_lessons_to_update = self.get_lessons_queryset().filter(
            period_schedule=instance.pk
        )

        for lesson in all_lessons_to_update:
            self.can_update_alone_lesson_by_fields(
                lesson,
                start_time=start_time,
                end_time=end_time,
                date=lesson.date,
                teacher=teacher,
                classroom=classroom,
                group=group,
            )

        return True
