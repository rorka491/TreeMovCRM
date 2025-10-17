# Выдает ошибку, связанную с duration
from django.test import TestCase
from datetime import date, time
from mainapp.models import Organization, User
from employers.models import Employer, Teacher, Department
from students.models import Student, StudentGroup
from lesson_schedule.models import Subject, Classroom, Schedule, Attendance, Grade


from django.test import TestCase
from mainapp.models import Organization, User

class BasicWorkingTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.org = Organization.objects.create(name="Working Test School", created_by=self.user)

        
        self.department = Department.objects.create(
            title="Преподаватели",
            code=100,
            org=self.org,
            created_by=self.user
        )
        
        self.employer = Employer.objects.create(
            name="Рабочий",
            surname="Преподаватель",
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
            name="Рабочий предмет",
            org=self.org,
            created_by=self.user
        )
        
        self.classroom = Classroom.objects.create(
            title="101",
            org=self.org,
            created_by=self.user
        )
        
        self.student = Student.objects.create(
            name="Рабочий",
            surname="Студент",
            birthday=date(2005, 5, 15),
            org=self.org,
            created_by=self.user
        )
        
        self.student_group = StudentGroup.objects.create(
            name="Рабочая группа",
            org=self.org,
            created_by=self.user
        )
        self.student_group.students.add(self.student)

    def test_schedule_creation_works(self):
        """Тест что создание занятия работает"""
        schedule = Schedule.objects.create(
            title="Рабочее занятие",
            date=date(2024, 1, 20),
            week_day=5,
            start_time=time(10, 0),
            end_time=time(11, 30),
            teacher=self.teacher,
            subject=self.subject,
            group=self.student_group,
            org=self.org,
            created_by=self.user
        )
        
        self.assertEqual(Schedule.objects.count(), 1)
        self.assertEqual(schedule.title, "Рабочее занятие")

    def test_attendance_creation_works(self):
        """Тест что создание посещения работает"""
        schedule = Schedule.objects.create(
            title="Занятие для посещения",
            date=date(2024, 1, 20),
            week_day=5,
            start_time=time(10, 0),
            end_time=time(11, 30),
            teacher=self.teacher,
            subject=self.subject,
            group=self.student_group,
            org=self.org,
            created_by=self.user
        )
        
        attendance = Attendance.objects.create(
            student=self.student,
            lesson=schedule,
            was_present=True,
            org=self.org,
            created_by=self.user
        )
        
        self.assertEqual(Attendance.objects.count(), 1)
        self.assertEqual(attendance.student, self.student)

    def test_grade_creation_works(self):
        """Тест что создание оценки работает"""
        schedule = Schedule.objects.create(
            title="Занятие для оценки",
            date=date(2024, 1, 20),
            week_day=5,
            start_time=time(10, 0),
            end_time=time(11, 30),
            teacher=self.teacher,
            subject=self.subject,
            group=self.student_group,
            org=self.org,
            created_by=self.user
        )
        
        grade = Grade.objects.create(
            student=self.student,
            lesson=schedule,
            value=5,
            comment="Отлично",
            org=self.org,
            created_by=self.user
        )
        
        self.assertEqual(Grade.objects.count(), 1)
        self.assertEqual(grade.value, 5)