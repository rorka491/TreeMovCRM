from django.test import TestCase
from students.models import Student, Parent, StudentGroup, Subscription
from datetime import date

class SimpleStudentsTest(TestCase):
    
    def test_student_creation(self):
        """Тест создания студента"""
        student = Student.objects.create(
            name="Иван",
            surname="Петров",
            birthday=date(2010, 5, 15),
            phone_number="79991234567"
        )
        self.assertEqual(student.name, "Иван")
        self.assertEqual(student.surname, "Петров")
        self.assertEqual(str(student), "Иван")

    def test_student_str_representation(self):
        """Тест строкового представления студента"""
        student = Student.objects.create(
            name="Мария",
            surname="Иванова",
            birthday=date(2011, 3, 20)
        )
        self.assertEqual(str(student), "Мария")

    def test_parent_creation(self):
        """Тест создания родителя"""
        parent = Parent.objects.create(
            name="Анна",
            surname="Петрова",
            phone_number="79997654321"
        )
        self.assertEqual(parent.name, "Анна")
        self.assertEqual(parent.surname, "Петрова")

    def test_parent_str_representation(self):
        """Тест строкового представления родителя"""
        parent = Parent.objects.create(
            name="Сергей",
            surname="Иванов"
        )
        self.assertEqual(str(parent), "Сергей Иванов")

    def test_student_group_creation(self):
        """Тест создания группы студентов"""
        group = StudentGroup.objects.create(
            name="Начинающие"
        )
        self.assertEqual(group.name, "Начинающие")

    def test_student_group_str_representation(self):
        """Тест строкового представления группы"""
        group = StudentGroup.objects.create(
            name="Продвинутые"
        )
        self.assertEqual(str(group), "Продвинутые")

    def test_subscription_creation(self):
        """Тест создания абонемента"""
        student = Student.objects.create(
            name="Алексей",
            surname="Сидоров",
            birthday=date(2012, 8, 10)
        )
        subscription = Subscription.objects.create(
            student=student,
            price=5000,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            is_active=True
        )
        self.assertEqual(subscription.price, 5000)
        self.assertTrue(subscription.is_active)