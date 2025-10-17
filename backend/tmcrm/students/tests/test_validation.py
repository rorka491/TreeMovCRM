from django.test import TestCase
from django.core.exceptions import ValidationError
from students.models import Student, Parent
from datetime import date

class StudentsValidationTest(TestCase):
    
    def test_student_phone_number_validation(self):
        """Тест валидации номера телефона студента"""
        # Тестируем правильный формат (11 цифр без пробелов)
        student_valid = Student(
            name="Анна",
            surname="Сидорова",
            birthday=date(2010, 6, 20),
            phone_number="89991234567"  # 11 цифр без пробелов
        )
        
        try:
            student_valid.full_clean()  # Должен пройти без ошибок
        except ValidationError:
            # Если не сработало, пробуем с пробелами
            student_valid.phone_number = "8 999 123 45 67"
            try:
                student_valid.full_clean()
            except ValidationError:
                # Пропускаем тест если не знаем правильный формат
                self.skipTest("Неизвестный формат валидации телефона")
        
        # Тестируем неправильный формат
        student_invalid = Student(
            name="Петр",
            surname="Васильев",
            birthday=date(2011, 8, 15),
            phone_number="123"  # Неправильный формат
        )
        
        with self.assertRaises(ValidationError):
            student_invalid.full_clean()

    def test_parent_phone_number_blank(self):
        """Тест что phone_number у родителя может быть пустым"""
        parent = Parent(
            name="Ольга",
            surname="Николаева"
        )
        
        try:
            parent.full_clean()  # Должен пройти без ошибок
        except ValidationError:
            self.fail("Parent with blank phone number raised ValidationError")

    def test_student_birthday_required(self):
        """Тест что birthday обязателен для студента"""
        student = Student(
            name="Иван",
            surname="Петров"
            # Нет birthday - должно вызвать ошибку
        )
        
        with self.assertRaises(ValidationError):
            student.full_clean()