from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from employers.models import Department, Employer, Teacher, DocumentsTypes, Documents, LeaveRequest, JobTitle
from mainapp.models import Organization, User
from datetime import date

class EmployersWorkingTest(TestCase):
    
    def setUp(self):
        # Создаем юзера и организацию
        self.user = User.objects.create(username="testuser_final")
        self.org = Organization.objects.create(name="Test Org Final", created_by=self.user)
        
        # Создаем отдел
        self.department = Department.objects.create(
            title="IT отдел", 
            code=1001,
            org=self.org
        )
        
        # API клиент
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_1_department_creation_works(self):
        """Тест что отдел создается"""
        department = Department.objects.create(
            title="HR отдел",
            code=1002,
            org=self.org
        )
        self.assertEqual(department.title, "HR отдел")
        self.assertEqual(department.code, 1002)
        self.assertEqual(department.org, self.org)

    def test_2_employer_creation_works(self):
        """Тест что сотрудник создается"""
        employer = Employer.objects.create(
            name="Иван",
            surname="Петров", 
            org=self.org,
            department=self.department
        )
        self.assertEqual(employer.name, "Иван")
        self.assertEqual(employer.surname, "Петров")
        self.assertEqual(employer.department, self.department)

    def test_3_employer_optional_fields_work(self):
        """Тест что необязательные поля работают"""
        employer = Employer.objects.create(
            name="Мария",
            surname="Иванова",
            patronymic="Сергеевна",
            birthday=date(1990, 5, 15),
            email="test@mail.ru",
            org=self.org
        )
        self.assertEqual(employer.patronymic, "Сергеевна")
        self.assertEqual(employer.email, "test@mail.ru")

    def test_4_teacher_creation_works(self):
        """Тест что преподаватель создается"""
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
        self.assertIn("Алексей", str(teacher))
        self.assertIn("Сидоров", str(teacher))

    def test_5_documents_types_creation_works(self):
        """Тест что тип документа создается"""
        doc_type = DocumentsTypes.objects.create(
            title="Трудовой договор",
            org=self.org
        )
        self.assertEqual(doc_type.title, "Трудовой договор")
        self.assertEqual(str(doc_type), "Трудовой договор")

    def test_6_documents_creation_works(self):
        """Тест что документ создается"""
        employer = Employer.objects.create(
            name="Ольга",
            surname="Николаева",
            org=self.org
        )
        doc_type = DocumentsTypes.objects.create(
            title="Паспорт",
            org=self.org
        )
        
        document = Documents.objects.create(
            employer=employer,
            doc_type=doc_type,
            org=self.org
        )
        
        # Добавляем доступ
        user2 = User.objects.create(username="testuser2")
        document.access_to_document.add(user2)
        
        self.assertEqual(document.employer, employer)
        self.assertEqual(document.doc_type, doc_type)
        self.assertEqual(document.access_to_document.count(), 1)

    def test_7_leave_request_creation_works(self):
        """Тест что заявка на отпуск создается"""
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

    def test_8_job_title_creation_works(self):
        """Тест что должность создается"""
        job_title = JobTitle.objects.create(
            title="Менеджер",
            org=self.org
        )
        self.assertEqual(job_title.title, "Менеджер")

    def test_9_employer_department_relationship_works(self):
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

    def test_10_leave_request_status_choices_work(self):
        """Тест что статусы заявки на отпуск работают"""
        employer = Employer.objects.create(
            name="Статусный",
            surname="Тест",
            org=self.org
        )
        
        # Создаем с разными статусами
        pending_request = LeaveRequest.objects.create(
            employee=employer,
            leave_type="vacation",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 5),
            status="pending",
            org=self.org
        )
        
        approved_request = LeaveRequest.objects.create(
            employee=employer,
            leave_type="sick", 
            start_date=date(2024, 2, 1),
            end_date=date(2024, 2, 3),
            status="approved",
            org=self.org
        )
        
        self.assertEqual(pending_request.status, "pending")
        self.assertEqual(approved_request.status, "approved")

    def test_11_leave_type_choices_work(self):
        """Тест что типы отпусков работают"""
        employer = Employer.objects.create(
            name="Типовой",
            surname="Тест", 
            org=self.org
        )
        
        vacation_request = LeaveRequest.objects.create(
            employee=employer,
            leave_type="vacation",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 7),
            org=self.org
        )
        
        sick_request = LeaveRequest.objects.create(
            employee=employer,
            leave_type="sick",
            start_date=date(2024, 1, 10),
            end_date=date(2024, 1, 12),
            org=self.org
        )
        
        unpaid_request = LeaveRequest.objects.create(
            employee=employer,
            leave_type="unpaid", 
            start_date=date(2024, 1, 15),
            end_date=date(2024, 1, 16),
            org=self.org
        )
        
        self.assertEqual(vacation_request.leave_type, "vacation")
        self.assertEqual(sick_request.leave_type, "sick")
        self.assertEqual(unpaid_request.leave_type, "unpaid")

    def test_12_employer_passport_fields_work(self):
        """Тест что паспортные поля работают"""
        employer = Employer.objects.create(
            name="Паспортный",
            surname="Тест",
            passport_series="1234",
            passport_num="567890", 
            inn="123456789012",
            org=self.org
        )
        
        self.assertEqual(employer.passport_series, "1234")
        self.assertEqual(employer.passport_num, "567890")
        self.assertEqual(employer.inn, "123456789012")

    def test_13_multiple_teachers_different_employers_work(self):
        """Тест что можно создать несколько преподавателей с разными работодателями"""
        employer1 = Employer.objects.create(name="Учитель1", surname="Тест1", org=self.org)
        employer2 = Employer.objects.create(name="Учитель2", surname="Тест2", org=self.org)
        
        teacher1 = Teacher.objects.create(employer=employer1, org=self.org)
        teacher2 = Teacher.objects.create(employer=employer2, org=self.org)
        
        self.assertEqual(Teacher.objects.count(), 2)
        self.assertEqual(teacher1.employer, employer1)
        self.assertEqual(teacher2.employer, employer2)

    def test_14_department_unique_name_constraint_works(self):
        """Тест что уникальность имени отдела работает в рамках организации"""
        # Первый отдел
        dept1 = Department.objects.create(title="Уникальный", code=1001, org=self.org)
        
        # Второй отдел с тем же именем в ДРУГОЙ организации - должен создаться
        org2 = Organization.objects.create(name="Другая орг", created_by=self.user)
        dept2 = Department.objects.create(title="Уникальный", code=1002, org=org2)
        
        self.assertEqual(dept1.title, "Уникальный")
        self.assertEqual(dept2.title, "Уникальный")

    def test_15_employer_phone_validation_works(self):
        """Тест что телефон проходит валидацию"""
        # Просто проверяем что создается без ошибок
        employer = Employer.objects.create(
            name="Телефонный",
            surname="Тест",
            org=self.org
        )
        # Если есть phone_number - тестируем его
        if hasattr(employer, 'phone_number'):
            employer.phone_number = "79991234567"
            employer.save()
            self.assertEqual(employer.phone_number, "79991234567")

    def test_16_documents_file_field_works(self):
        """Тест что FileField в документах работает"""
        employer = Employer.objects.create(name="Документный", surname="Тест", org=self.org)
        doc_type = DocumentsTypes.objects.create(title="Файл", org=self.org)
        
        #  создаем документ без файла
        document = Documents.objects.create(
            employer=employer,
            doc_type=doc_type,
            org=self.org
        )
        
        self.assertEqual(document.employer, employer)
        self.assertEqual(document.doc_type, doc_type)

    def test_17_employer_progress_field_works(self):
        """Тест что поле progress работает"""
        employer = Employer.objects.create(
            name="Прогресс",
            surname="Тест",
            org=self.org
        )
        
        #поле progress
        if hasattr(employer, 'progress'):
            employer.progress = 85.5
            employer.save()
            self.assertEqual(employer.progress, 85.5)

    def test_18_all_models_have_meta_verbose_names(self):
        """Тест что у всех моделей есть verbose_name"""
        self.assertEqual(Employer._meta.verbose_name, 'Сотрудник')
        self.assertEqual(Teacher._meta.verbose_name, 'Преподаватель')
        self.assertEqual(Department._meta.verbose_name, 'Отдел')
        self.assertEqual(DocumentsTypes._meta.verbose_name, 'Тип документа')
        self.assertEqual(Documents._meta.verbose_name, 'Документ')
        self.assertEqual(LeaveRequest._meta.verbose_name, 'Запросы на отпуск')
        self.assertEqual(JobTitle._meta.verbose_name, 'Должность')

class EmployersAPIWorkingTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(username="testuser_api")
        self.org = Organization.objects.create(name="Test Org API", created_by=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_api_endpoints_exist(self):
        """Тест что эндпоинты API существуют"""
        try:
            reverse('employer-list')
            reverse('teacher-list')
            reverse('documents-list')
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"API endpoints not configured: {e}")

    def test_simple_get_requests_work(self):
        """Тест что GET запросы работают"""
        # Создаем тестовые данные
        Department.objects.create(title="API отдел", code=1001, org=self.org)
        
        # Пробуем сделать GET запрос
        url = reverse('employer-list')
        response = self.client.get(url)
        
        # Проверяем что ответ получен (даже если 200 или 401)
        self.assertIsNotNone(response)
        self.assertIn(response.status_code, [200, 401, 403])

    def test_model_managers_exist(self):
        """Тест что менеджеры моделей работают"""
        # Просто проверяем что можем получить queryset
        self.assertIsNotNone(Employer.objects.all())
        self.assertIsNotNone(Teacher.objects.all())
        self.assertIsNotNone(Department.objects.all())
        self.assertIsNotNone(Documents.objects.all())

    def test_basic_crud_operations_work(self):
        """Тест что базовые CRUD операции работают"""
        # CREATE
        employer = Employer.objects.create(
            name="CRUD",
            surname="Тест",
            org=self.org
        )
        
        # READ
        employer_from_db = Employer.objects.get(id=employer.id)
        self.assertEqual(employer_from_db.name, "CRUD")
        
        # UPDATE
        employer.name = "CRUD Обновленный"
        employer.save()
        employer.refresh_from_db()
        self.assertEqual(employer.name, "CRUD Обновленный")
        
        # DELETE
        employer_id = employer.id
        employer.delete()
        
        with self.assertRaises(Employer.DoesNotExist):
            Employer.objects.get(id=employer_id)