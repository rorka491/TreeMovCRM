# Выдает ошибку, связанную с duration
from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, time
from mainapp.models import Organization, User
from employers.models import Employer, Teacher, Department
from students.models import Student, StudentGroup
from lesson_schedule.models import Subject, Classroom, Schedule


from django.test import TestCase
from mainapp.models import Organization, User

class ScheduleValidationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.org = Organization.objects.create(name="Validation Test School", created_by=self.user)    
        self.department = Department.objects.create(
            title="Преподаватели",
            code=100,
            org=self.org,
            created_by=self.user
        )
        
        self.employer = Employer.objects.create(
            name="Валидация",
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
            name="Валидационный предмет",
            org=self.org,
            created_by=self.user
        )
        
        self.classroom = Classroom.objects.create(
            title="101",
            org=self.org,
            created_by=self.user
        )
        
        self.student_group = StudentGroup.objects.create(
            name="Валидационная группа",
            org=self.org,
            created_by=self.user
        )

    def test_schedule_invalid_time(self):
        """Тест невалидного времени (конец раньше начала)"""
        schedule = Schedule(
            title="Невалидное время",
            date=date(2024, 1, 15),
            week_day=1,
            start_time=time(11, 0),
            end_time=time(10, 0),  # Конец раньше начала
            teacher=self.teacher,
            subject=self.subject,
            group=self.student_group,
            org=self.org,
            created_by=self.user
        )
        
        with self.assertRaises(ValidationError):
            schedule.clean()

    def test_schedule_time_conflict(self):
        """Тест конфликта времени занятий"""
        # Первое занятие
        Schedule.objects.create(
            title="Первое занятие",
            date=date(2024, 1, 15),
            week_day=1,
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=self.teacher,
            subject=self.subject,
            group=self.student_group,
            org=self.org,
            created_by=self.user
        )
        
        # Конфликтующее занятие
        conflicting_schedule = Schedule(
            title="Конфликтующее занятие",
            date=date(2024, 1, 15),
            week_day=1,
            start_time=time(9, 0),  # Точно такое же время
            end_time=time(10, 30),
            teacher=self.teacher,  # Тот же преподаватель
            subject=self.subject,
            group=self.student_group,
            org=self.org,
            created_by=self.user
        )
        
        # Должна быть вызвана ошибка валидации
        with self.assertRaises(ValidationError):
            conflicting_schedule.full_clean()