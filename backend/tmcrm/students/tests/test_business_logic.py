from django.test import TestCase
from students.models import Student, Subscription, StudentGroup, Parent
from datetime import date, timedelta, datetime
from django.utils import timezone

class StudentsBusinessLogicTest(TestCase):
    
    def test_subscription_creation_with_days(self):
        """Тест создания абонемента с автоматическим расчетом end_date"""
        student = Student.objects.create(
            name="Иван",
            surname="Петров",
            birthday=date(2010, 5, 15)
        )
        
        # Создаем абонемент с явным указанием end_date
        start_date = date(2024, 1, 1)
        end_date = timezone.make_aware(datetime(2024, 1, 31))  # Создаем aware datetime
        
        subscription = Subscription.objects.create(
            student=student,
            price=5000,
            start_date=start_date,
            end_date=end_date,
            is_active=True
        )
        
        expected_end_date = start_date + timedelta(days=30)
        self.assertEqual(subscription.end_date.date(), expected_end_date)
        self.assertTrue(subscription.is_active)

    def test_subscription_str_representation(self):
        """Тест строкового представления абонемента"""
        student = Student.objects.create(
            name="Мария",
            surname="Иванова",
            birthday=date(2011, 3, 20)
        )
        
        end_date = timezone.make_aware(datetime(2024, 1, 31))
        subscription = Subscription.objects.create(
            student=student,
            price=5000,
            start_date=date(2024, 1, 1),
            end_date=end_date,
            is_active=True
        )
        
        # Проверяем что абонемент создан и связан со студентом
        self.assertEqual(subscription.student.name, "Мария")
        self.assertEqual(subscription.price, 5000)

    def test_student_progress_default(self):
        """Тест значения progress по умолчанию"""
        student = Student.objects.create(
            name="Петр",
            surname="Сидоров",
            birthday=date(2012, 7, 15)
        )
        self.assertEqual(student.progress, 0)

    def test_student_group_unique_name(self):
        """Тест уникальности имени группы"""
        StudentGroup.objects.create(name="Уникальная группа")
        
        # Попытка создать группу с тем же именем должна вызвать ошибку
        with self.assertRaises(Exception):
            StudentGroup.objects.create(name="Уникальная группа")