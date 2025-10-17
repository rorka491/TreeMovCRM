from django.test import TestCase
from students.models import Student, Parent, StudentGroup, Subscription
from datetime import date, datetime
from django.utils import timezone

class StudentsRelationshipsTest(TestCase):
    
    def test_student_group_relationships(self):
        """Тест связей студентов с группами"""
        # Создаем студентов
        student1 = Student.objects.create(
            name="Иван",
            surname="Петров",
            birthday=date(2010, 5, 15)
        )
        student2 = Student.objects.create(
            name="Мария", 
            surname="Иванова",
            birthday=date(2011, 3, 20)
        )
        
        # Создаем группу
        group = StudentGroup.objects.create(name="Начинающие")
        
        # Добавляем студентов в группу
        group.students.add(student1, student2)
        
        # Проверяем связи - ИСПРАВЛЕННАЯ ЛОГИКА
        self.assertEqual(group.students.count(), 2)
        self.assertIn(student1, group.students.all())
        self.assertIn(student2, group.students.all())  # student2 должен быть в группе
        self.assertIn(group, student1.groups.all())    # группа должна быть у student1

    def test_student_multiple_groups(self):
        """Тест принадлежности студента к нескольким группам"""
        student = Student.objects.create(
            name="Алексей",
            surname="Сидоров", 
            birthday=date(2012, 8, 10)
        )
        
        group1 = StudentGroup.objects.create(name="Начинающие")
        group2 = StudentGroup.objects.create(name="Спортивные")
        
        student.groups.add(group1, group2)
        
        self.assertEqual(student.groups.count(), 2)
        self.assertIn(group1, student.groups.all())
        self.assertIn(group2, student.groups.all())

    def test_parent_child_relationships(self):
        """Тест связей родителей с детьми"""
        student = Student.objects.create(
            name="Дарья",
            surname="Кузнецова",
            birthday=date(2010, 12, 5)
        )
        
        parent = Parent.objects.create(
            name="Елена",
            surname="Кузнецова",
            phone_number="89991357924"  # ИСПРАВЛЕНО: 11 цифр без пробелов
        )
        
        # Связываем родителя и ребенка
        parent.child.add(student)
        
        # Проверяем связи
        self.assertEqual(parent.child.count(), 1)
        self.assertIn(student, parent.child.all())
        self.assertEqual(student.parents.count(), 1)
        self.assertIn(parent, student.parents.all())

    def test_multiple_parents_per_student(self):
        """Тест нескольких родителей у одного студента"""
        student = Student.objects.create(
            name="Артем",
            surname="Попов",
            birthday=date(2011, 4, 18)
        )
        
        parent1 = Parent.objects.create(name="Ольга", surname="Попова")
        parent2 = Parent.objects.create(name="Игорь", surname="Попов")
        
        student.parents.add(parent1, parent2)
        
        self.assertEqual(student.parents.count(), 2)
        self.assertIn(parent1, student.parents.all())
        self.assertIn(parent2, student.parents.all())

    def test_student_subscription_relationships(self):
        """Тест связей студента с абонементами"""
        student = Student.objects.create(
            name="Михаил",
            surname="Федоров",
            birthday=date(2010, 7, 22)
        )
        
        end_date = timezone.make_aware(datetime(2024, 1, 31))
        subscription = Subscription.objects.create(
            student=student,
            price=6000,
            start_date=date(2024, 1, 1),
            end_date=end_date
        )
        
        # Проверяем связи
        self.assertEqual(student.subscriptions.count(), 1)
        self.assertEqual(subscription.student, student)
        self.assertIn(subscription, student.subscriptions.all())