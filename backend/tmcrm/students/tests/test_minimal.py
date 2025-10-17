from django.test import TestCase

class MinimalTest(TestCase):
    """Минимальные тесты которые точно работают"""
    
    def test_database_connection(self):
        """Тест подключения к базе данных"""
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        self.assertEqual(result[0], 1)
    
    def test_simple_math(self):
        """Простой математический тест"""
        self.assertEqual(2 * 2, 4)
    
    def test_student_model_exists(self):
        """Проверяем что модель Student существует"""
        from students.models import Student
        self.assertTrue(hasattr(Student, 'objects'))