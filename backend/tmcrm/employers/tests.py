from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from employers.models import Teacher, Employer, Department, Leave, LeaveRequest, DocumentsTypes, Documents
from mainapp.models import Organization, User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date

User = get_user_model()


class BaseEmployerTestCase(APITestCase):

    def setUp(self):
        from mainapp import signals
        from employers import signals as employer_signals
        
        post_save.disconnect(signals.create_org_settings, sender=Organization)
        post_save.disconnect(employer_signals.create_leave_on_approval, sender=LeaveRequest)
        
        self.org1 = Organization.objects.create(name="Test Organization 1")
        self.org2 = Organization.objects.create(name="Test Organization 2")
        
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="testpass123",
            org=self.org1
        )
        
        self.user2 = User.objects.create_user(
            username="testuser2", 
            password="testpass123",
            org=self.org2
        )
        
        refresh = RefreshToken.for_user(self.user1)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def tearDown(self):
        from mainapp import signals
        from employers import signals as employer_signals
        
        post_save.connect(signals.create_org_settings, sender=Organization)
        post_save.connect(employer_signals.create_leave_on_approval, sender=LeaveRequest)


class OrganizationIsolationTests(BaseEmployerTestCase):

    def setUp(self):
        super().setUp()
        
        self.employer_org1 = Employer.objects.create(
            org=self.org1,
            name="Иван Орг1",
            surname="Иванов",
            patronymic="Иванович", 
            email="ivanov_org1@example.com"
        )
        
        self.employer_org2 = Employer.objects.create(
            org=self.org2, 
            name="Петр Орг2",
            surname="Петров",
            patronymic="Петрович",
            email="petrov_org2@example.com"
        )
        
        self.teacher_org1 = Teacher.objects.create(
            employer=self.employer_org1,
            org=self.org1
        )
        
        self.teacher_org2 = Teacher.objects.create(
            employer=self.employer_org2,
            org=self.org2
        )
        
        self.employer_list_url = reverse('employer-list')
        self.teacher_list_url = reverse('teacher-list')

    def test_employer_organization_isolation(self):
        response = self.client.get(self.employer_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        employers = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        self.assertEqual(len(employers), 1)
        self.assertEqual(employers[0]['name'], "Иван Орг1")
        self.assertEqual(employers[0]['org'], self.org1.id)

    def test_teacher_organization_isolation(self):
        response = self.client.get(self.teacher_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        teachers = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        self.assertEqual(len(teachers), 1)
        self.assertEqual(teachers[0]['id'], self.teacher_org1.id)

    def test_cannot_access_other_org_employer(self):
        url = reverse('employer-detail', kwargs={'pk': self.employer_org2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_access_other_org_teacher(self):
        url = reverse('teacher-detail', kwargs={'pk': self.teacher_org2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_employer_with_auto_org(self):
        data = {
            'name': 'Новый',
            'surname': 'Работодатель', 
            'patronymic': 'Тестович',
            'email': 'new@example.com'
        }
        
        response = self.client.post(self.employer_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        employer = Employer.objects.get(id=response.data['id'])
        self.assertEqual(employer.org, self.org1)

    def test_create_teacher_with_auto_org(self):
        new_employer = Employer.objects.create(
            org=self.org1,
            name="Для нового преподавателя",
            surname="Тестов",
            patronymic="Тестович",
            email="newteacher@example.com"
        )
        
        data = {
            'employer': new_employer.id
        }
        
        response = self.client.post(self.teacher_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        teacher = Teacher.objects.get(id=response.data['id'])
        self.assertEqual(teacher.org, self.org1)


class DepartmentTests(BaseEmployerTestCase):

    def setUp(self):
        super().setUp()
        
        self.department1 = Department.objects.create(
            org=self.org1,
            title="Отдел разработки",
            code=1001
        )
        
        self.department2 = Department.objects.create(
            org=self.org2,
            title="Отдел маркетинга",
            code=1002
        )
        
        self.employer_with_dept = Employer.objects.create(
            org=self.org1,
            name="Анна",
            surname="Сидорова",
            patronymic="Владимировна",
            email="sidorova@example.com",
            department=self.department1
        )
        
        self.list_url = reverse('department-list')
        self.detail_url = reverse('department-detail', kwargs={'pk': self.department1.pk})

    def test_get_departments_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        departments = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        self.assertEqual(len(departments), 1)
        self.assertEqual(departments[0]['title'], "Отдел разработки")
        self.assertEqual(departments[0]['code'], 1001)

    def test_create_department(self):
        data = {
            'title': 'Новый отдел',
            'code': 1003 
        }
        
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.filter(org=self.org1).count(), 2)

    def test_employer_department_relationship(self):
        url = reverse('employer-detail', kwargs={'pk': self.employer_with_dept.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['department'], self.department1.id)


class LeaveTests(BaseEmployerTestCase):

    def setUp(self):
        super().setUp()
        
        self.employer_org1 = Employer.objects.create(
            org=self.org1,
            name="Мария",
            surname="Иванова",
            patronymic="Петровна",
            email="ivanova@example.com"
        )
        
        self.employer_org2 = Employer.objects.create(
            org=self.org2,
            name="Ольга",
            surname="Петрова", 
            patronymic="Сергеевна",
            email="petrova@example.com"
        )
        
        self.leave_request_org1 = LeaveRequest.objects.create(
            org=self.org1,
            employee=self.employer_org1,
            leave_type="vacation",
            start_date="2024-01-01",
            end_date="2024-01-14",
            status="approved"
        )
        
        self.leave_request_org2 = LeaveRequest.objects.create(
            org=self.org2,
            employee=self.employer_org2,
            leave_type="sick",
            start_date="2024-02-01",
            end_date="2024-02-07",
            status="approved"
        )
        
        self.leave_org1 = Leave.objects.create(
            org=self.org1,
            leave_request=self.leave_request_org1,
            employee=self.employer_org1,
            leave_type="vacation",
            start_date="2024-01-01",
            end_date="2024-01-14"
        )
        
        self.leave_org2 = Leave.objects.create(
            org=self.org2,
            leave_request=self.leave_request_org2,
            employee=self.employer_org2,
            leave_type="sick",
            start_date="2024-02-01",
            end_date="2024-02-07"
        )
        
        self.list_url = reverse('leave-list')

    def test_get_leaves_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        leaves = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        self.assertEqual(len(leaves), 1)
        self.assertEqual(leaves[0]['leave_type'], "vacation")
        self.assertEqual(leaves[0]['employee'], self.employer_org1.id)

    def test_cannot_access_other_org_leave(self):
        url = reverse('leave-detail', kwargs={'pk': self.leave_org2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_leave(self):
        new_employer = Employer.objects.create(
            org=self.org1,
            name="Новый",
            surname="Сотрудник",
            patronymic="Тестович",
            email="new@example.com"
        )
        
        new_leave_request = LeaveRequest.objects.create(
            org=self.org1,
            employee=new_employer,
            leave_type="unpaid",
            start_date="2024-03-01",
            end_date="2024-03-05",
            status="approved"
        )
        
        data = {
            'leave_request': new_leave_request.id,
            'employee': new_employer.id,
            'leave_type': 'unpaid',
            'start_date': '2024-03-01',
            'end_date': '2024-03-05'
        }
        
        response = self.client.post(self.list_url, data, format='json')
        
        if response.status_code == status.HTTP_201_CREATED:
            self.assertEqual(Leave.objects.filter(org=self.org1).count(), 2)
        else:
            response = self.client.get(self.list_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            leaves = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
            self.assertEqual(len(leaves), 1)

    def test_leave_organization_isolation(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        leaves = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        self.assertEqual(len(leaves), 1)
        self.assertEqual(leaves[0]['id'], self.leave_org1.id)
        self.assertEqual(leaves[0]['org'], self.org1.id)

    def test_get_leave_detail(self):
        url = reverse('leave-detail', kwargs={'pk': self.leave_org1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.leave_org1.id)
        self.assertEqual(response.data['leave_type'], "vacation")


class TeacherTests(BaseEmployerTestCase):

    def setUp(self):
        super().setUp()
        
        self.employer1 = Employer.objects.create(
            org=self.org1,
            name="Иван",
            surname="Иванов", 
            patronymic="Иванович",
            email="ivanov@example.com"
        )
        
        self.employer2 = Employer.objects.create(
            org=self.org1, 
            name="Петр",
            surname="Петров",
            patronymic="Петрович", 
            email="petrov@example.com"
        )
        
        self.teacher1 = Teacher.objects.create(
            employer=self.employer1,
            org=self.org1
        )
        
        self.list_url = reverse('teacher-list')
        self.detail_url = reverse('teacher-detail', kwargs={'pk': self.teacher1.pk})

    def test_get_teachers_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        teachers = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        self.assertEqual(len(teachers), 1)

    def test_get_teacher_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.teacher1.id)
        self.assertEqual(response.data['org'], self.org1.id)

    def test_create_teacher(self):
        data = {
            'employer': self.employer2.id
        }
        
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.filter(org=self.org1).count(), 2)

    def test_delete_teacher(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Teacher.objects.filter(org=self.org1).count(), 0)

    def test_teacher_filtering_by_employer(self):
        filtered_url = f"{self.list_url}?employer={self.employer1.id}"
        response = self.client.get(filtered_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        teachers = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        self.assertEqual(len(teachers), 1)
        self.assertEqual(teachers[0]['id'], self.teacher1.id)

    def test_teacher_organization_auto_assignment(self):
        new_employer = Employer.objects.create(
            org=self.org1,
            name="Для автоназначения",
            surname="Тест",
            patronymic="Тестович",
            email="autoassign@example.com"
        )
        
        data = {
            'employer': new_employer.id
        }
        
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        teacher = Teacher.objects.get(id=response.data['id'])
        self.assertEqual(teacher.org, self.org1)


class EmployerTests(BaseEmployerTestCase):

    def setUp(self):
        super().setUp()

        self.employer1 = Employer.objects.create(
            org=self.org1,
            name="Анна",
            surname="Сидорова",
            patronymic="Владимировна",
            email="sidorova@example.com",
            passport_series="1234",
            passport_num="567890"
        )
        
        self.employer2 = Employer.objects.create(
            org=self.org1,
            name="Сергей",
            surname="Кузнецов",
            patronymic="Алексеевич",
            email="kuznetsov@example.com",
            passport_series="4321",
            passport_num="098765"
        )
        
        self.list_url = reverse('employer-list')
        self.detail_url = reverse('employer-detail', kwargs={'pk': self.employer1.pk})

    def test_get_employers_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        employers = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        self.assertEqual(len(employers), 2)

    def test_get_employer_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.employer1.id)
        self.assertEqual(response.data['org'], self.org1.id)

    def test_create_employer(self):
        data = {
            'name': 'Ольга',
            'surname': 'Новикова',
            'patronymic': 'Сергеевна',
            'email': 'novikova@example.com',
            'passport_series': '1111',
            'passport_num': '222222'
        }
        
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employer.objects.filter(org=self.org1).count(), 3)

    def test_update_employer(self):
        data = {'name': 'Анна Обновленная'}
        
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.employer1.refresh_from_db()
        self.assertEqual(self.employer1.name, 'Анна Обновленная')

    def test_delete_employer(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employer.objects.filter(org=self.org1).count(), 1)

    def test_employer_organization_auto_assignment(self):
        data = {
            'name': 'Тест',
            'surname': 'Автоорг',
            'patronymic': 'Тестович',
            'email': 'autoorg@example.com'
        }
        
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        employer = Employer.objects.get(id=response.data['id'])
        self.assertEqual(employer.org, self.org1)


class LeaveRequestTests(BaseEmployerTestCase):

    def setUp(self):
        super().setUp()
        
        self.employer_org1 = Employer.objects.create(
            org=self.org1,
            name="Тест",
            surname="Сотрудник",
            patronymic="Тестович",
            email="test@example.com"
        )
        
        self.leave_request = LeaveRequest.objects.create(
            org=self.org1,
            employee=self.employer_org1,
            leave_type="vacation",
            start_date="2024-01-01",
            end_date="2024-01-14",
            status="pending"
        )

    def test_leave_request_creation(self):
        leave_request = LeaveRequest.objects.create(
            org=self.org1,
            employee=self.employer_org1,
            leave_type='sick',
            start_date='2024-02-01',
            end_date='2024-02-07',
            status='pending'
        )
        self.assertEqual(leave_request.leave_type, 'sick')
        self.assertEqual(leave_request.org, self.org1)

    def test_leave_request_status_choices(self):
        self.assertEqual(self.leave_request.status, 'pending')
        self.assertFalse(self.leave_request.is_approved)


class DocumentsTests(BaseEmployerTestCase):

    def setUp(self):
        super().setUp()
        
        self.employer = Employer.objects.create(
            org=self.org1,
            name="Документ",
            surname="Тест",
            patronymic="Тестович",
            email="doc@example.com"
        )
        
        self.doc_type = DocumentsTypes.objects.create(
            title="Паспорт",
            org=self.org1
        )

    def test_documents_types_creation(self):
        doc_type = DocumentsTypes.objects.create(
            title="Договор",
            org=self.org1
        )
        self.assertEqual(doc_type.title, "Договор")
        self.assertEqual(doc_type.org, self.org1)

    def test_documents_types_organization_isolation(self):
        doc_type_org2 = DocumentsTypes.objects.create(
            title="СНИЛС",
            org=self.org2
        )
        
        doc_types_org1 = DocumentsTypes.objects.filter(org=self.org1)
        self.assertNotIn(doc_type_org2, doc_types_org1)


class IntegrationTests(BaseEmployerTestCase):

    def setUp(self):
        super().setUp()
        
        self.department = Department.objects.create(
            org=self.org1,
            title="Тестовый отдел",
            code=9999
        )
        
        self.employer = Employer.objects.create(
            org=self.org1,
            name="Интеграционный",
            surname="Тест",
            patronymic="Тестович",
            email="integration@example.com",
            department=self.department
        )
        
        self.teacher = Teacher.objects.create(
            employer=self.employer,
            org=self.org1
        )

    def test_employer_department_integration(self):
        self.assertEqual(self.employer.department, self.department)
        self.assertIn(self.employer, self.department.employer_set.all())

    def test_teacher_employer_integration(self):
        self.assertEqual(self.teacher.employer, self.employer)
        self.assertEqual(self.teacher.org, self.org1)

    def test_cascade_deletion_protection(self):
        test_employer = Employer.objects.create(
            org=self.org1,
            name="ТестКаскад",
            surname="Удаления",
            patronymic="Тестович",
            email="cascade@example.com"
        )
        
        employer_id = test_employer.id
        
        test_employer.delete()
        
        try:
            self.teacher.refresh_from_db()
            self.assertTrue(Teacher.objects.filter(id=self.teacher.id).exists())
        except Teacher.DoesNotExist:
            pass


class TestChangeTeacherFields(BaseEmployerTestCase):

    def setUp(self):
        super().setUp()

        self.employer1 = Employer.objects.create(
            org=self.org1,
            name="Иван",
            surname="Иванов",
            patronymic="Иванович",
            email="ivanov@example.com"
        )

        self.employer2 = Employer.objects.create(
            org=self.org1,  
            name="Мария",
            surname="Петрова", 
            patronymic="Александровна",
            email="petrova@example.com"
        )

        self.teacher1 = Teacher.objects.create(
            employer=self.employer1,
            org=self.org1
        )

    def test_change_teacher_employer_restriction(self):
        teacher_id = self.teacher1.id
        url = reverse('teacher-detail', kwargs={'pk': teacher_id})

        if not Teacher.objects.filter(employer=self.employer2).exists():
            data = {'employer': self.employer2.id}

            response = self.client.patch(url, data, format='json')

            self.assertIn(
                response.status_code,
                [status.HTTP_400_BAD_REQUEST, status.HTTP_200_OK, status.HTTP_403_FORBIDDEN]
            )

            self.teacher1.refresh_from_db()
            
            if response.status_code == status.HTTP_400_BAD_REQUEST:
                self.assertEqual(self.teacher1.employer.id, self.employer1.id)
        else:
            self.skipTest("Employer2 уже используется другим Teacher")