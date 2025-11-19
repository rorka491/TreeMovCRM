from __future__ import annotations
from django.db.models import Q
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError
from mainapp.serializers import BaseSerializerExcludeFields
from lesson_schedule.models import Lesson
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
    """
    Миксин для валидации расписания уроков в ViewSet'ах.

    Предназначен для повторного использования в представлениях,
    работающих с расписаниями (Lesson). Обеспечивает удобные методы
    для извлечения связанных уроков, получения ключевых полей урока и
    проверки возможности обновления уроков без конфликтов.

    Требуется реализовать метод `get_lessons_queryset()` в ViewSet-е,
    чтобы миксин мог выполнять выборки данных.

    Основные возможности:
    - Проверка возможности обновления одного урока без пересечений.
    - Массовая проверка уроков в рамках периодического расписания.
    - Выдача свободных слотов при невозможности изменения.
    """

    def get_lessons_queryset(self) -> QuerySet[Lesson]:
        """
        Метод должен быть реализован в viewset-классе.
        Используется для получения списка уроков, подлежащих валидации.
        """
        raise NotImplementedError(
            "Метод get_lessons_queryset должен быть реализован в viewset-классе"
        )

    def _get_related_lessons(self, serializer) -> QuerySet[Lesson]:
        """
        Возвращает все связанные сериальные уроки,
        принадлежащие одной периодической записи расписания и не завершённые.

        Args:
            serializer: Сериализатор с экземпляром урока.

        Returns:
            QuerySet[Lesson]: Запрос с уроками, связанными через поле period_schedule
            и помеченными как незавершённые (is_completed=False).
        """
        return self.get_lessons_queryset().filter(
            period_schedule=serializer.instance.pk, is_completed=False
        )

    def _extract_lesson_fields(self, serializer) -> dict[str, Any]:
        """
        Извлекает ключевые поля урока из сериализатора,
        используя новые данные, если они есть,
        иначе берёт значения из текущего экземпляра.

        Параметры:
            serializer: Сериализатор, содержащий валидированные данные и экземпляр урока.

        Возвращает:
            Словарь с полями: start_time, end_time, teacher, classroom, group.
        """
        instance = serializer.instance
        new_data = serializer.validated_data

        return {
            "start_time": new_data.get("start_time", instance.start_time),
            "end_time": new_data.get("end_time", instance.end_time),
            "teacher": new_data.get("teacher", instance.teacher),
            "classroom": new_data.get("classroom", instance.classroom),
            "group": new_data.get("group", instance.group),
        }

    def can_update_alone_lesson_by_fields(
        self,
        instance,
        *,  # Делает так что все аргументы после будут исключитеьно именованные
        start_time,
        end_time,
        date,
        teacher,
        classroom,
        group,
    ):
        """
        Проверяет, можно ли обновить указанный урок с заданными параметрами без пересечения с другими уроками.
        Метод ищет все уроки на тот же день, где учитель, аудитория или группа совпадают с переданными параметрами,
        исключая текущий урок. Затем он проверяет, не пересекается ли заданное время с другими занятиями.
        Если пересечений нет — возвращает True.
        Если пересечения есть — возбуждает ValidationError с информацией о свободных слотах и текущем дне.
        """
        all_lessons_at_day = (
            self.get_lessons_queryset()
            .filter(date=date)
            .filter(Q(teacher=teacher) | Q(classroom=classroom) | Q(group=group))
            .exclude(pk=instance.pk)
        )

        lesson_list = [
            LessonSlot(lesson.start_time, lesson.end_time)
            for lesson in all_lessons_at_day
        ]

        current_lesson = LessonSlot(start_time, end_time)

        if LessonSlot.can_add_lesson(lesson_list, current_lesson):
            return True
        else:
            slots = LessonSlot.find_free_slots_at_day(lesson_list)
            raise ValidationError({
                "detail": "Невозможно обновить время урока на заданное время",
                "free_slots": [f"{s[0]} - {s[1]}" for s in slots],
                "lesson_list": [str(lesson) for lesson in lesson_list],
                "current_date": date.isoformat(),
            })

    def can_update_alone_lesson(
        self,
        serializer: BaseSerializerExcludeFields,
        is_force_update=False,
    ):
        if is_force_update:
            return True

        fields = self._extract_lesson_fields(serializer=serializer)
        lesson = serializer.instance
        return self.can_update_alone_lesson_by_fields(
            lesson, date=lesson.date, **fields
        )

    def can_update_period_lesson(
        self, serializer: BaseSerializerExcludeFields, is_force_update=False
    ):
        if is_force_update:
            return True

        all_lessons_to_update = self._get_related_lessons(serializer=serializer)
        
        fields = self._extract_lesson_fields(serializer=serializer)
        for lesson in all_lessons_to_update:
            self.can_update_alone_lesson_by_fields(lesson, date=lesson.date, **fields)

        return True