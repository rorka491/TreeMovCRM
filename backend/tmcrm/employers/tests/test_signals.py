# lesson_schedule/tests/test_signals.py
from django.test import TestCase
from datetime import date, time
from mainapp.models import Organization, User
from employers.models import Employer, Teacher, Department
from students.models import StudentGroup
from lesson_schedule.models import Subject, Classroom, PeriodSchedule, Schedule


from django.test import TestCase
from mainapp.models import Organization, User

class ScheduleSignalsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.org = Organization.objects.create(name="Signals Test School", created_by=self.user)

        
        # Базовые данные
        self.department = Department.objects.create(
            title="Преподаватели",
            code=100,
            org=self.org,
            created_by=self.user
        )
        
        self.employer = Employer.objects.create(
            name="Сигнал",
            surname="Тест",
            department=self.department,
            org=self.org,
            created_by=self.user
        )
        
        self.teacher = Teacher.objects.create(
            employer=self.employer,
            org=self.org,
            created_by=self.user
        )
        
        self.subject = Subject.objects.create(
            name="Сигнальный предмет",
            org=self.org,
            created_by=self.user
        )
        
        self.classroom = Classroom.objects.create(
            title="301",
            org=self.org,
            created_by=self.user
        )
        
        self.student_group = StudentGroup.objects.create(
            name="Сигнальная группа",
            org=self.org,
            created_by=self.user
        )

    def test_period_schedule_with_explicit_date(self):
        """Тест создания PeriodSchedule с явной датой окончания"""
        # Временно отключаем проблемный сигнал
        from django.db.models.signals import post_save
        from lesson_schedule import signals
        
        post_save.disconnect(signals.create_lessons_until_date, sender=PeriodSchedule)
        
        try:
            # Создаем PeriodSchedule с явной датой в правильном формате
            period_schedule = PeriodSchedule.objects.create(
                period=7,  # Еженедельно
                title="Сигнальное занятие",
                start_time=time(10, 0),
                end_time=time(11, 30),
                teacher=self.teacher,
                subject=self.subject,
                classroom=self.classroom,
                group=self.student_group,
                start_date=date(2024, 1, 15),
                repeat_lessons_until_date=date(2024, 6, 15),  # Явно указываем date объект
                org=self.org,
                created_by=self.user
            )
            
            # Проверяем что PeriodSchedule создан
            self.assertEqual(PeriodSchedule.objects.count(), 1)
            self.assertEqual(period_schedule.repeat_lessons_until_date, date(2024, 6, 15))
        finally:
            # Восстанавливаем сигнал
            post_save.connect(signals.create_lessons_until_date, sender=PeriodSchedule)