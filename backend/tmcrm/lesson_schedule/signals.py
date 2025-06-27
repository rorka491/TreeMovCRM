from lesson_schedule.models import Schedule, PeriodSchedule
from django.dispatch import receiver
from django.db.models.signals import post_save, post_migrate
from datetime import timedelta
from mainapp.utils import checkout_interval_schedule_table



@receiver(post_save, sender=PeriodSchedule)
def create_lessons_until_date(sender, created, instance, **kwargs):
    if created:
        user_settings = instance.created_by.settings
        # Получаем дату продлеиня занятий если нет то берем эту дату из настроек
        repeat_until = getattr(instance, 'repeat_lessons_until_date', None) 
        if not repeat_until:
            repeat_until = user_settings.repeat_lessons_until

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
                new_lesson = Schedule(
                    date=current_date,
                    created_by=instance.created_by,
                    week_day=current_date.isoweekday(),
                    period_schedule=instance,
                    **data
                )
                lessons_to_create.append(new_lesson)
                current_date += timedelta(days=period)

            Schedule.objects.bulk_create(lessons_to_create)
        else:
            raise ValueError('не указана периодичность')
        


@receiver(post_save, sender=PeriodSchedule)
def update_data_not_complete_lessons(sender, created, instance, **kwargs):
    if not created:
        lessons = Schedule.objects.filter(period_schedule=instance, is_completed=False)

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
    from .utils import create_update_complete_lessons_task
    create_update_complete_lessons_task()


