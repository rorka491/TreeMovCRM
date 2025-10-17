from django.test import TestCase
from employers.models import Employer, Teacher, Department, Documents, DocumentsTypes
from mainapp.models import Organization, User
from datetime import date

class EmployersBasicViewsTest(TestCase):
    """Базовые тесты views без сложной аутентификации и API"""

    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.org = Organization.objects.create(name="Test Org", created_by=self.user)
        self.department = Department.objects.create(
            title="IT отдел", 
            code=1001,
            org=self.org
        )

    def test_employer_creation_logic(self):
        """Тест логики создания сотрудника (без API)"""
        employer = Employer.objects.create(
            name="Тест",
            surname="Сотрудник",
            org=self.org
        )
        self.assertEqual(Employer.objects.count(), 1)
        self.assertEqual(employer.name, "Тест")

    def test_teacher_creation_logic(self):
        """Тест логики создания преподавателя (без API)"""
        employer = Employer.objects.create(
            name="Преподаватель",
            surname="Тест",
            org=self.org
        )
        teacher = Teacher.objects.create(employer=employer, org=self.org)
        self.assertEqual(Teacher.objects.count(), 1)
        self.assertEqual(teacher.employer, employer)

    def test_documents_creation_logic(self):
        """Тест логики создания документа (без API)"""
        employer = Employer.objects.create(
            name="Документ",
            surname="Тест",
            org=self.org
        )
        doc_type = DocumentsTypes.objects.create(
            title="Тестовый тип",
            org=self.org
        )
        document = Documents.objects.create(
            employer=employer,
            doc_type=doc_type,
            org=self.org
        )
        self.assertEqual(Documents.objects.count(), 1)
        self.assertEqual(document.employer, employer)


class EmployersModelRelationsTest(TestCase):
    """Тесты связей между моделями"""

    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.org = Organization.objects.create(name="Test Org", created_by=self.user)

    def test_employer_department_relationship(self):
        """Тест связи сотрудник-отдел"""
        department = Department.objects.create(
            title="Тестовый отдел",
            code=999,
            org=self.org
        )
        employer = Employer.objects.create(
            name="Сотрудник",
            surname="Отдела", 
            department=department,
            org=self.org
        )
        
        self.assertEqual(employer.department, department)
        self.assertIn(employer, department.employer_set.all())

    def test_teacher_employer_relationship(self):
        """Тест связи преподаватель-сотрудник"""
        employer = Employer.objects.create(
            name="Учитель",
            surname="Тест",
            org=self.org
        )
        teacher = Teacher.objects.create(employer=employer, org=self.org)
        
        self.assertEqual(teacher.employer, employer)

    def test_documents_access_relationship(self):
        """Тест связи документ-пользователь"""
        employer = Employer.objects.create(
            name="Документный",
            surname="Сотрудник",
            org=self.org
        )
        doc_type = DocumentsTypes.objects.create(
            title="Доступ",
            org=self.org
        )
        user = User.objects.create(username="testuser2", org=self.org)
        
        document = Documents.objects.create(
            employer=employer,
            doc_type=doc_type,
            org=self.org
        )
        document.access_to_document.add(user)
        
        self.assertEqual(document.access_to_document.count(), 1)
        self.assertIn(user, document.access_to_document.all())


class EmployersValidationTest(TestCase):
    """Тесты валидации данных"""

    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.org = Organization.objects.create(name="Test Org", created_by=self.user)

    def test_employer_required_fields(self):
        """Тест обязательных полей сотрудника"""
        # Должен создаться без ошибок
        employer = Employer.objects.create(
            name="Обязательный",
            surname="Тест",
            org=self.org
        )
        self.assertIsNotNone(employer.id)

    def test_employer_optional_fields(self):
        """Тест необязательных полей сотрудника"""
        employer = Employer.objects.create(
            name="Опциональный",
            surname="Тест",
            patronymic="Отчество",
            birthday=date(1990, 1, 1),
            email="test@example.com",
            passport_series="1234",
            passport_num="567890",
            inn="123456789012",
            org=self.org
        )
        self.assertEqual(employer.patronymic, "Отчество")
        self.assertEqual(employer.email, "test@example.com")


class EmployersBusinessLogicTest(TestCase):
    """Тесты бизнес-логики"""

    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.org = Organization.objects.create(name="Test Org", created_by=self.user)

    def test_employer_string_representation(self):
        """Тест строкового представления сотрудника"""
        employer = Employer.objects.create(
            name="Строковый",
            surname="Тест",
            org=self.org
        )
        # Проверяем что строка содержит имя и фамилию
        self.assertIn("Строковый", str(employer))
        self.assertIn("Тест", str(employer))

    def test_teacher_string_representation(self):
        """Тест строкового представления преподавателя"""
        employer = Employer.objects.create(
            name="Преподавательский",
            surname="Тест",
            org=self.org
        )
        teacher = Teacher.objects.create(employer=employer, org=self.org)
        self.assertIn("Преподавательский", str(teacher))
        self.assertIn("Тест", str(teacher))

    def test_department_creation_and_fields(self):
        """Тест создания отдела и его полей (без проверки __str__)"""
        department = Department.objects.create(
            title="Тестовый отдел",
            code=1001,
            org=self.org
        )
        self.assertEqual(department.title, "Тестовый отдел")
        self.assertEqual(department.code, 1001)
        # Не проверяем __str__ так как его нет в модели

    def test_documents_types_string_representation(self):
        """Тест строкового представления типа документа"""
        doc_type = DocumentsTypes.objects.create(
            title="Трудовой договор",
            org=self.org
        )
        self.assertEqual(str(doc_type), "Трудовой договор")