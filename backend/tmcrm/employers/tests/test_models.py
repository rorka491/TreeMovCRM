from django.test import TestCase
from django.core.exceptions import ValidationError
from employers.models import Department, Employer, Teacher, JobTitle, LeaveRequest, DocumentsTypes, Documents
from mainapp.models import Organization, User
from datetime import date

class EmployersModelsTest(TestCase):

    def setUp(self):
        # Создаем уникального пользователя для каждого теста
        self.user = User.objects.create(username="testuser_models")
        self.org = Organization.objects.create(name="Test Org", created_by=self.user)
        self.department = Department.objects.create(
            title="IT отдел", 
            code=1001,
            org=self.org
        )

    def test_department_creation(self):
        """Тест создания отдела"""
        department = Department.objects.create(
            title="HR отдел",
            code=1002,
            org=self.org
        )
        self.assertEqual(department.title, "HR отдел")
        self.assertEqual(department.code, 1002)

    def test_employer_creation(self):
        """Тест создания сотрудника"""
        employer = Employer.objects.create(
            name="Иван",
            surname="Петров",
            patronymic="Сергеевич",
            birthday=date(1990, 5, 15),
            department=self.department,
            email="ivan@test.ru",
            org=self.org
        )
        self.assertEqual(employer.name, "Иван")
        self.assertEqual(employer.surname, "Петров")
        self.assertEqual(employer.patronymic, "Сергеевич")
        self.assertTrue("Иван" in str(employer))
        self.assertTrue("Петров" in str(employer))

    def test_employer_optional_fields(self):
        """Тест создания сотрудника с необязательными полями"""
        employer = Employer.objects.create(
            name="Мария",
            surname="Иванова",
            org=self.org
        )
        self.assertIsNone(employer.patronymic)
        self.assertIsNone(employer.birthday)
        self.assertIsNone(employer.department)

    def test_teacher_creation(self):
        """Тест создания преподавателя"""
        employer = Employer.objects.create(
            name="Алексей",
            surname="Сидоров",
            org=self.org
        )
        teacher = Teacher.objects.create(
            employer=employer,
            org=self.org
        )
        self.assertEqual(teacher.employer, employer)
        self.assertEqual(str(teacher), "Алексей Сидоров")

    def test_leave_request_creation(self):
        """Тест создания запроса на отпуск"""
        employer = Employer.objects.create(
            name="Петр",
            surname="Васильев",
            org=self.org
        )
        leave_request = LeaveRequest.objects.create(
            employee=employer,
            leave_type="vacation",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 14),
            status="pending",
            org=self.org
        )
        self.assertEqual(leave_request.employee, employer)
        self.assertEqual(leave_request.leave_type, "vacation")
        self.assertEqual(leave_request.status, "pending")
        self.assertEqual(str(leave_request), "vacation")

    def test_documents_types_creation(self):
        """Тест создания типа документа"""
        doc_type = DocumentsTypes.objects.create(
            title="Трудовой договор",
            org=self.org
        )
        self.assertEqual(doc_type.title, "Трудовой договор")
        self.assertEqual(str(doc_type), "Трудовой договор")

    def test_documents_creation(self):
        """Тест создания документа"""
        employer = Employer.objects.create(
            name="Ольга",
            surname="Николаева",
            org=self.org
        )
        doc_type = DocumentsTypes.objects.create(
            title="Паспорт",
            org=self.org
        )
        # Создаем уникального пользователя для этого теста
        user = User.objects.create(username="testuser_documents")
        
        document = Documents.objects.create(
            employer=employer,
            doc_type=doc_type,
            org=self.org
        )
        document.access_to_document.add(user)
        
        self.assertEqual(document.employer, employer)
        self.assertEqual(document.doc_type, doc_type)
        self.assertEqual(document.access_to_document.count(), 1)

    def test_employer_passport_validation(self):
        """Тест валидации паспортных данных"""
        employer = Employer.objects.create(
            name="Дмитрий",
            surname="Кузнецов",
            passport_series="1234",
            passport_num="567890",
            inn="123456789012",
            org=self.org
        )
        self.assertEqual(employer.passport_series, "1234")
        self.assertEqual(employer.passport_num, "567890")
        self.assertEqual(employer.inn, "123456789012")

    def test_leave_type_choices(self):
        """Тест доступных типов отпусков"""
        # Используем прямое сравнение со строковыми значениями
        self.assertEqual(LeaveRequest.leave_type.field.choices[0][0], "vacation")
        self.assertEqual(LeaveRequest.leave_type.field.choices[1][0], "sick")
        self.assertEqual(LeaveRequest.leave_type.field.choices[2][0], "unpaid")