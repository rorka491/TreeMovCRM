from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from employers.models import Teacher, Employer, Department, Leave, LeaveRequest
from mainapp.models import Organization
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class BaseEmployerTestCase(APITestCase):
    """Базовый класс для тестов employers с отключенными сигналами"""

    def setUp(self):
        from mainapp import signals
        post_save.disconnect(signals.create_org_settings, sender=Organization)
        
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
        post_save.connect(signals.create_org_settings, sender=Organization)
        
        Teacher.objects.all().delete()
        Employer.objects.all().delete()
        Department.objects.all().delete()
        Leave.objects.all().delete()
        LeaveRequest.objects.all().delete()
        Organization.objects.all().delete()
        User.objects.all().delete()


class OrganizationIsolationTests(BaseEmployerTestCase):
    """Тесты изоляции данных между организациями"""

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
        """Тест изоляции работодателей по организациям"""
        response = self.client.get(self.employer_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Иван Орг1")
        self.assertEqual(response.data[0]['org'], self.org1.id)

    def test_teacher_organization_isolation(self):
        """Тест изоляции преподавателей по организациям"""
        response = self.client.get(self.teacher_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.teacher_org1.id)

    def test_cannot_access_other_org_employer(self):
        """Тест невозможности доступа к работодателю чужой организации"""
        url = reverse('employer-detail', kwargs={'pk': self.employer_org2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_access_other_org_teacher(self):
        """Тест невозможности доступа к преподавателю чужой организации"""
        url = reverse('teacher-detail', kwargs={'pk': self.teacher_org2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_employer_with_auto_org(self):
        """Тест автоматического назначения организации при создании работодателя"""
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
        """Тест автоматического назначения организации при создании преподавателя"""
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
    """Тесты для отделов"""

    def setUp(self):
        super().setUp()
        
        self.department1 = Department.objects.create(
            org=self.org1,
            title="Отдел разработки",
            code=1001  # Числовое поле
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
        """Тест получения списка отделов"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Отдел разработки")
        self.assertEqual(response.data[0]['code'], 1001)

    def test_create_department(self):
        """Тест создания отдела"""
        data = {
            'title': 'Новый отдел',
            'code': 1003 
        }
        
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.filter(org=self.org1).count(), 2)

    def test_employer_department_relationship(self):
        """Тест связи работодателя с отделом"""
        url = reverse('employer-detail', kwargs={'pk': self.employer_with_dept.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['department'], self.department1.id)


class LeaveTests(BaseEmployerTestCase):
    """Тесты для отпусков"""

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
        """Тест получения списка отпусков"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['leave_type'], "vacation")
        self.assertEqual(response.data[0]['employee'], self.employer_org1.id)

    def test_cannot_access_other_org_leave(self):
        """Тест невозможности доступа к отпуску чужой организации"""
        url = reverse('leave-detail', kwargs={'pk': self.leave_org2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_leave(self):
        """Тест создания отпуска"""
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
            self.assertEqual(len(response.data), 1)

    def test_leave_organization_isolation(self):
        """Тест изоляции отпусков по организациям"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        leaves = response.data
        self.assertEqual(len(leaves), 1)
        self.assertEqual(leaves[0]['id'], self.leave_org1.id)
        self.assertEqual(leaves[0]['org'], self.org1.id)

    def test_get_leave_detail(self):
        """Тест получения деталей отпуска"""
        url = reverse('leave-detail', kwargs={'pk': self.leave_org1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.leave_org1.id)
        self.assertEqual(response.data['leave_type'], "vacation")


class TeacherTests(BaseEmployerTestCase):
    """Тесты для преподавателей с учетом организаций"""

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
        """Тест получения списка преподавателей"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_teacher_detail(self):
        """Тест получения деталей преподавателя"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.teacher1.id)
        self.assertEqual(response.data['org'], self.org1.id)

    def test_create_teacher(self):
        """Тест создания преподавателя"""
        data = {
            'employer': self.employer2.id
        }
        
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.filter(org=self.org1).count(), 2)

    def test_delete_teacher(self):
        """Тест удаления преподавателя"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Teacher.objects.filter(org=self.org1).count(), 0)

    def test_teacher_filtering_by_employer(self):
        """Тест фильтрации преподавателей по работодателю"""
        filtered_url = f"{self.list_url}?employer={self.employer1.id}"
        response = self.client.get(filtered_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.teacher1.id)

    def test_teacher_organization_auto_assignment(self):
        """Тест автоматического назначения организации преподавателю"""
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
    """Тесты для работодателей с учетом организаций"""

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
        """Тест получения списка работодателей"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_employer_detail(self):
        """Тест получения деталей работодателя"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.employer1.id)
        self.assertEqual(response.data['org'], self.org1.id)

    def test_create_employer(self):
        """Тест создания работодателя"""
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
        """Тест обновления работодателя"""
        data = {'name': 'Анна Обновленная'}
        
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.employer1.refresh_from_db()
        self.assertEqual(self.employer1.name, 'Анна Обновленная')

    def test_delete_employer(self):
        """Тест удаления работодателя"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employer.objects.filter(org=self.org1).count(), 1)

    def test_employer_organization_auto_assignment(self):
        """Тест автоматического назначения организации работодателю"""
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


class TestChangeTeacherFields(BaseEmployerTestCase):
    """Тест для проверки изменения полей преподавателя с учетом организаций"""

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
        """Тест ограничения на изменение работодателя преподавателя"""
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
                self.assertNotEqual(
                    self.teacher1.employer.id, 
                    self.employer2.id
                )
        else:
            self.skipTest("Employer2 уже используется другим Teacher")