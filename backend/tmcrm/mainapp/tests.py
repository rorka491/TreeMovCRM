from datetime import date, time
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.test import APITestCase
from .models import Organization
from employers.models import Employer, Teacher
from students.models import Student, StudentGroup
from lesson_schedule.models import Lesson, Classroom, Subject
from .services.orgs import create_user_with_org
from auth.tokens import token
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
from lesson_schedule.serializers.read import ScheduleReadSerializer
from rest_framework.test import force_authenticate
from rest_framework.test import APIClient

User = get_user_model()

class BaseSetupDB(APITestCase):
     

    def _get_access_token(self):
        user = User.objects.get(username="testuser")
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return access_token

    def setUp(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    @classmethod
    def setUpTestData(cls) -> None:
        # Организация
        cls.org = Organization.objects.create(name="Test_Org")

        cls.user = create_user_with_org(
            org=cls.org, password="pass123", username="testuser"
        )

        cls.employer1 = Employer.create_manager.create(
            org=cls.org,
            name="Иван",
            surname="Иванов",
            patronymic="Иванович",
            birthday="1985-05-12",
            email="ivan.ivanov@example.com",
            passport_series="1234",
            passport_num="567890",
            inn="123456789012",
            department=None,
            created_by=cls.user,
        )

        cls.employer2 = Employer.create_manager.create(
            org=cls.org,
            name="Мария",
            surname="Петрова",
            patronymic="Александровна",
            birthday="1990-08-23",
            email="maria.petrova@example.com",
            passport_series="4321",
            passport_num="098765",
            inn="210987654321",
            department=None,
            created_by=cls.user,
        )

        cls.teacher1: Teacher = Teacher.objects.create(
            employer=cls.employer1, org=cls.org, created_by=cls.user
        )

        cls.teacher2: Teacher = Teacher.objects.create(
            employer=cls.employer2, org=cls.org, created_by=cls.user
        )

        cls.subject = Subject.create_manager.create(
            org=cls.org, name="Математика", created_by=cls.user
        )
        cls.subject.teacher.set(
            [
                cls.teacher1,
                cls.teacher2,
            ]
        )

        cls.classroom1 = Classroom.create_manager.create(
            org=cls.org, title="445", created_by=cls.user
        )

        cls.classroom2 = Classroom.create_manager.create(
            org=cls.org, title="446", created_by=cls.user
        )

        cls.student1 = Student.create_manager.create(
            org=cls.org,
            name="Алексей",
            surname="Смирнов",
            progress=87.50,
            phone_number="79001234567",
            birthday=date(2005, 3, 15),
            email="alexey.smirnov@example.com",
            created_by=cls.user,
        )

        cls.student2 = Student.create_manager.create(
            org=cls.org,
            name="Марина",
            surname="Иванова",
            progress=92.00,
            phone_number="79007654321",
            birthday=date(2006, 7, 10),
            email="marina.ivanova@example.com",
            created_by=cls.user,
        )

        cls.group1 = StudentGroup.create_manager.create(
            org=cls.org, name="TestGroup1", created_by=cls.user
        )
        cls.group1.students.set(
            [
                cls.student1,
            ]
        )

        cls.group2 = StudentGroup.create_manager.create(
            org=cls.org, name="TestGroup2", created_by=cls.user
        )
        cls.group2.students.set(
            [
                cls.student2,
            ]
        )

        cls.schedule1 = Lesson.create_manager.create(
            teacher=cls.teacher1,
            subject=cls.subject,
            group=cls.group1,
            classroom=cls.classroom1,
            title="Test lesson1",
            date=date(2025, 8, 9),
            week_day=6,
            is_canceled=False,
            is_completed=False,
            start_time="12:00:00",
            end_time="13:30:00",
            org=cls.org,
            created_by=cls.user,
        )
        cls.schedule2 = Lesson.create_manager.create(
            teacher=cls.teacher2,
            subject=cls.subject,
            group=cls.group2,
            classroom=cls.classroom2,
            title="Test lesson2",
            date=date(2025, 8, 9),
            week_day=6,
            is_canceled=False,
            is_completed=False,
            start_time="13:00:00",
            end_time="14:00:00",
            org=cls.org,
            created_by=cls.user,
        )
        cls.schedule3 = Lesson.create_manager.create(
            teacher=cls.teacher1,
            subject=cls.subject,
            group=cls.group1,
            classroom=cls.classroom1,
            title="Test lesson3",
            date=date(2025, 8, 9),
            week_day=6,
            is_canceled=False,
            is_completed=False,
            start_time="13:50:00",
            end_time="15:00:00",
            org=cls.org,
            created_by=cls.user,
        )



class TestSignals(BaseSetupDB):

    def test_settings_signal(self):                      
        url=f'/api/'
        self.client.post(url=url, data=data, format="json")