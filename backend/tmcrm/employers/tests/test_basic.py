# lesson_schedule/tests/test_basic.py
from django.test import TestCase
from datetime import date, time
from mainapp.models import Organization, User
from lesson_schedule.models import Subject


from django.test import TestCase
from mainapp.models import Organization, User

class BasicScheduleTest(TestCase):
    
    def test_basic_organization_creation(self):
        """Базовый тест создания организации"""
        user = User.objects.create(username="testuser")
        org = Organization.objects.create(name="Basic Test Org", created_by=user)
        self.assertEqual(org.name, "Basic Test Org")
    
    def test_basic_user_creation(self):
        """Базовый тест создания пользователя"""
        user = User.objects.create(username="testuser")
        org = Organization.objects.create(name="User Test Org", created_by=user)
        user2 = User.objects.create(username="testuser2", org=org)
        self.assertEqual(user2.username, "testuser2")
    
    def test_basic_subject_creation(self):
        """Базовый тест создания предмета"""
        user = User.objects.create(username="testuser")
        org = Organization.objects.create(name="Subject Test Org", created_by=user)
        # Дальше тестируйте создание предметов...
        
        subject = Subject.objects.create(
            name="Базовый предмет",
            org=org,
            created_by=user
        )
        
        self.assertEqual(subject.name, "Базовый предмет")
        self.assertEqual(subject.org, org)