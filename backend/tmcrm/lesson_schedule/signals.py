from __future__ import annotations
from lesson_schedule.models import Lesson, PeriodLesson
from django.dispatch import receiver
from django.db.models.signals import post_save, post_migrate, pre_save
from datetime import timedelta
from mainapp.utils import checkout_interval_schedule_table
from .models import Attendance, Grade


@receiver(post_save, sender=PeriodLesson)
def create_lessons_until_date(sender, created, instance, **kwargs):
    if created:
        org_settings = instance.org.settings
        # Получаем дату продлеиня занятий если нет то берем эту дату из настроек
        repeat_until = getattr(instance, 'repeat_lessons_until_date', None) 
        if not repeat_until:
            repeat_until = org_settings.repeat_lessons_until

        period = instance.period
        current_date = instance.start_date

        # получение атрибутов экземпляра чтобы на его омнове создать другие
        data = {f.name: getattr(instance, f.name) 
                for f in instance._meta.fields 
                if f.name not in ('date', 'created_by', 'id', 'period', 'repeat_lessons_until_date', 'start_date', 'title')}

        if period:
            lessons_to_create = []
            # Цикл отвечает за создание списка, 
            while current_date <= repeat_until:
                new_lesson = Lesson(
                    date=current_date,
                    created_by=instance.created_by,
                    week_day=current_date.isoweekday(),
                    period_schedule=instance,
                    **data
                )
                lessons_to_create.append(new_lesson)
                current_date += timedelta(days=period)

            Lesson.objects.bulk_create(lessons_to_create)
        else:
            raise ValueError('не указана периодичность')


@receiver(post_save, sender=PeriodLesson)
def update_data_not_complete_lessons(sender, created, instance, **kwargs):
    if not created:
        lessons = Lesson.objects.filter(period_schedule=instance, is_completed=False)

        data = {
            f.name: getattr(instance, f.name)
            for f in instance._meta.fields
            if f.name not in ('date', 'created_by', 'id', 'period', 'repeat_lessons_until_date', 'start_date', 'title')
            and getattr(instance, f.name) is not None
        }
        

        lessons.update(**data)


@receiver(post_migrate)
@checkout_interval_schedule_table
def setup_periodic_tasks(sender, **kwargs):
    from .utils import (
        init_task_create_update_complete_lessons_task,
        init_task_create_attendences_for_all_passes,
    )
    init_task_create_update_complete_lessons_task()
    init_task_create_attendences_for_all_passes()
    


@receiver(pre_save, sender=Attendance)
def set_attendance_date(sender, instance, **kwargs) -> None:
    if instance.lesson and instance.lesson.date:
        instance.date = instance.lesson.date

@receiver(pre_save, sender=Grade)
def set_grade_date(sender, instance, **kwargs):
    if instance.lesson and instance.lesson.date:
        instance.date = instance.lesson.date