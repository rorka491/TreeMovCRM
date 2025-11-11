# signals.py - ИСПРАВЬТЕ функцию create_lessons_until_date
from __future__ import annotations
from lesson_schedule.models import Schedule, PeriodSchedule
from django.dispatch import receiver
from django.db.models.signals import post_save, post_migrate, pre_save
from datetime import timedelta, datetime
from mainapp.utils import checkout_interval_schedule_table
from .models import Attendance, Grade
from django.core.exceptions import ValidationError


@receiver(post_save, sender=PeriodSchedule)
def create_lessons_until_date(sender, instance, created, **kwargs):
    if created:
        org_settings = instance.org.settings
        repeat_until = getattr(instance, 'repeat_lessons_until_date', None) 
        if not repeat_until:
            repeat_until = org_settings.repeat_lessons_until
            
            # Если repeat_until - строка, преобразуем в дату
            if isinstance(repeat_until, str):
                try:
                    current_year = datetime.now().year
                    repeat_until = datetime.strptime(f"{current_year}-{repeat_until}", "%Y-%m-%d").date()
                except ValueError:
                    repeat_until = instance.start_date + timedelta(days=180)

        period = instance.period
        current_date = instance.start_date

        if not period:
            raise ValueError('не указана периодичность')

        data = {f.name: getattr(instance, f.name) 
                for f in instance._meta.fields 
                if f.name not in ('id', 'created_by', 'period', 'repeat_lessons_until_date', 'start_date') 
                and getattr(instance, f.name) is not None}

        lessons_to_create = []
        # Создаем занятия до конечной даты
        while current_date <= repeat_until:
            new_lesson = Schedule(
                date=current_date,
                created_by=instance.created_by,
                week_day=current_date.isoweekday(),  
                period_schedule=instance,
                **data
            )
            
            try:
                new_lesson.full_clean()
                lessons_to_create.append(new_lesson)
            except ValidationError:
                pass
                
            current_date += timedelta(days=period)

        if lessons_to_create:
            Schedule.objects.bulk_create(lessons_to_create)

@receiver(post_save, sender=PeriodSchedule)
def update_data_not_complete_lessons(sender, instance, created, **kwargs):
    if not created:
        lessons = Schedule.objects.filter(period_schedule=instance, is_completed=False)
        
        # Обновляем ВСЕ поля, включая title
        update_fields = {}
        for field in instance._meta.fields:
            if field.name not in ('id', 'created_by', 'period', 'repeat_lessons_until_date', 'start_date'):
                value = getattr(instance, field.name)
                if value is not None:  
                    update_fields[field.name] = value
        
        if update_fields:
            lessons.update(**update_fields)


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