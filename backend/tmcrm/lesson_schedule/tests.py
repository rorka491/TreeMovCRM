from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from lesson_schedule.models import Schedule, Subject, Classroom, PeriodSchedule, Attendance, Grade
from students.models import StudentGroup, Student
from employers.models import Teacher, Employer
from mainapp.models import Organization
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date, time, timedelta, datetime

User = get_user_model()


class BaseScheduleTestCase(APITestCase):
    """Базовый класс для тестов расписания с отключенными сигналами"""

    def setUp(self):
        # Временно отключаем сигналы, которые вызывают ошибки
        from mainapp import signals as main_signals
        post_save.disconnect(main_signals.create_org_settings, sender=Organization)
        
        # Отключаем сигналы lesson_schedule если они есть
        try:
            from lesson_schedule import signals as schedule_signals
            post_save.disconnect(schedule_signals.create_lessons_until_date, sender=PeriodSchedule)
        except ImportError:
            pass
        
        # Создаем несколько организаций для тестирования
        self.org1 = Organization.objects.create(name="Test Organization 1")
        self.org2 = Organization.objects.create(name="Test Organization 2")
        
        # Создаем пользователей для разных организаций
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
        
        # Создаем работодателей и преподавателей
        self.employer1_org1 = Employer.objects.create(
            org=self.org1,
            name="Иван",
            surname="Иванов",
            patronymic="Иванович",
            email="ivanov@example.com"
        )
        
        self.employer2_org1 = Employer.objects.create(
            org=self.org1,
            name="Петр",
            surname="Петров",
            patronymic="Петрович",
            email="petrov@example.com"
        )
        
        self.employer1_org2 = Employer.objects.create(
            org=self.org2,
            name="Сергей",
            surname="Сергеев",
            patronymic="Сергеевич",
            email="sergeev@example.com"
        )
        
        self.teacher1_org1 = Teacher.objects.create(
            employer=self.employer1_org1,
            org=self.org1
        )
        
        self.teacher2_org1 = Teacher.objects.create(
            employer=self.employer2_org1,
            org=self.org1
        )
        
        self.teacher1_org2 = Teacher.objects.create(
            employer=self.employer1_org2,
            org=self.org2
        )
        
        # Создаем предметы
        self.subject1_org1 = Subject.objects.create(
            org=self.org1,
            name="Математика"
        )
        
        self.subject2_org1 = Subject.objects.create(
            org=self.org1,
            name="Физика"
        )
        
        self.subject1_org2 = Subject.objects.create(
            org=self.org2,
            name="Химия"
        )
        
        # Создаем аудитории
        self.classroom1_org1 = Classroom.objects.create(
            org=self.org1,
            title="101",
            floor=1
        )
        
        self.classroom2_org1 = Classroom.objects.create(
            org=self.org1,
            title="102",
            floor=1
        )
        
        self.classroom1_org2 = Classroom.objects.create(
            org=self.org2,
            title="201",
            floor=2
        )
        
        # Создаем группы студентов
        self.group1_org1 = StudentGroup.objects.create(
            org=self.org1,
            name="Группа 1А"
        )
        
        self.group2_org1 = StudentGroup.objects.create(
            org=self.org1,
            name="Группа 1Б"
        )
        
        self.group1_org2 = StudentGroup.objects.create(
            org=self.org2,
            name="Группа 2А"
        )
        
        # Создаем расписания
        self.schedule1_org1 = Schedule.objects.create(
            org=self.org1,
            title="Урок математики",
            date=date(2024, 1, 15),
            week_day=1,
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=self.teacher1_org1,
            classroom=self.classroom1_org1,
            group=self.group1_org1,
            subject=self.subject1_org1,
            lesson=1
        )
        
        self.schedule2_org1 = Schedule.objects.create(
            org=self.org1,
            title="Урок физики",
            date=date(2024, 1, 15),
            week_day=1,
            start_time=time(10, 45),
            end_time=time(12, 15),
            teacher=self.teacher2_org1,
            classroom=self.classroom2_org1,
            group=self.group2_org1,
            subject=self.subject2_org1,
            lesson=2
        )
        
        self.schedule1_org2 = Schedule.objects.create(
            org=self.org2,
            title="Урок химии",
            date=date(2024, 1, 15),
            week_day=1,
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=self.teacher1_org2,
            classroom=self.classroom1_org2,
            group=self.group1_org2,
            subject=self.subject1_org2,
            lesson=1
        )
        
        # Аутентифицируем первого пользователя по умолчанию
        refresh = RefreshToken.for_user(self.user1)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def tearDown(self):
        # Восстанавливаем сигналы после теста
        from mainapp import signals as main_signals
        post_save.connect(main_signals.create_org_settings, sender=Organization)
        
        # Восстанавливаем сигналы lesson_schedule если они есть
        try:
            from lesson_schedule import signals as schedule_signals
            post_save.connect(schedule_signals.create_lessons_until_date, sender=PeriodSchedule)
        except ImportError:
            pass
        
        # Очищаем все созданные объекты
        Schedule.objects.all().delete()
        Subject.objects.all().delete()
        Classroom.objects.all().delete()
        PeriodSchedule.objects.all().delete()
        Attendance.objects.all().delete()
        Grade.objects.all().delete()
        StudentGroup.objects.all().delete()
        Teacher.objects.all().delete()
        Employer.objects.all().delete()
        Organization.objects.all().delete()
        User.objects.all().delete()


class OrganizationIsolationTests(BaseScheduleTestCase):
    """Тесты изоляции данных между организациями"""

    def setUp(self):
        super().setUp()
        
        self.schedule_list_url = reverse('schedule-list')
        self.subject_list_url = reverse('subject-list')
        self.classroom_list_url = reverse('classroom-list')

    def test_schedule_organization_isolation(self):
        """Тест изоляции расписаний по организациям"""
        response = self.client.get(self.schedule_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Должны видеть только расписания своей организации
        self.assertEqual(len(response.data), 2)
        schedule_ids = [schedule['id'] for schedule in response.data]
        self.assertIn(self.schedule1_org1.id, schedule_ids)
        self.assertIn(self.schedule2_org1.id, schedule_ids)
        self.assertNotIn(self.schedule1_org2.id, schedule_ids)

    def test_subject_organization_isolation(self):
        """Тест изоляции предметов по организациям"""
        response = self.client.get(self.subject_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Должны видеть только предметы своей организации
        self.assertEqual(len(response.data), 2)
        subject_names = [subject['name'] for subject in response.data]
        self.assertIn("Математика", subject_names)
        self.assertIn("Физика", subject_names)
        self.assertNotIn("Химия", subject_names)

    def test_classroom_organization_isolation(self):
        """Тест изоляции аудиторий по организациям"""
        response = self.client.get(self.classroom_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Должны видеть только аудитории своей организации
        self.assertEqual(len(response.data), 2)
        classroom_titles = [classroom['title'] for classroom in response.data]
        self.assertIn("101", classroom_titles)
        self.assertIn("102", classroom_titles)
        self.assertNotIn("201", classroom_titles)

    def test_cannot_access_other_org_schedule(self):
        """Тест невозможности доступа к расписанию чужой организации"""
        url = reverse('schedule-detail', kwargs={'pk': self.schedule1_org2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_access_other_org_subject(self):
        """Тест невозможности доступа к предмету чужой организации"""
        url = reverse('subject-detail', kwargs={'pk': self.subject1_org2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_access_other_org_classroom(self):
        """Тест невозможности доступа к аудитории чужой организации"""
        url = reverse('classroom-detail', kwargs={'pk': self.classroom1_org2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ScheduleTests(BaseScheduleTestCase):
    """Тесты для расписаний"""

    def setUp(self):
        super().setUp()
        
        self.list_url = reverse('schedule-list')
        self.detail_url = reverse('schedule-detail', kwargs={'pk': self.schedule1_org1.pk})

    def test_get_schedules_list(self):
        """Тест получения списка расписаний"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_schedule_detail(self):
        """Тест получения деталей расписания"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.schedule1_org1.id)
        self.assertEqual(response.data['title'], "Урок математики")
        self.assertEqual(response.data['org'], self.org1.id)

    def test_create_schedule(self):
        """Тест создания расписания"""
        data = {
            'title': 'Новый урок',
            'date': '2024-01-16',
            'start_time': '13:00:00',
            'end_time': '14:30:00',
            'teacher': self.teacher1_org1.id,
            'classroom': self.classroom1_org1.id,
            'group': self.group1_org1.id,
            'subject': self.subject1_org1.id,
            'lesson': 3
        }
        
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_schedule(self):
        """Тест обновления расписания"""
        data = {'title': 'Обновленный урок математики'}
        
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.schedule1_org1.refresh_from_db()
        self.assertEqual(self.schedule1_org1.title, 'Обновленный урок математики')

    def test_delete_schedule(self):
        """Тест удаления расписания"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Schedule.objects.filter(org=self.org1).count(), 1)

    def test_schedule_organization_auto_assignment(self):
        """Тест автоматического назначения организации расписанию"""
        data = {
            'title': 'Автоназначенный урок',
            'date': '2024-01-17',
            'start_time': '15:00:00',
            'end_time': '16:30:00',
            'teacher': self.teacher1_org1.id,
            'classroom': self.classroom1_org1.id,
            'group': self.group1_org1.id,
            'subject': self.subject1_org1.id
        }
        
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_schedule_filtering_by_date(self):
        """Тест фильтрации расписаний по дате"""
        filtered_url = f"{self.list_url}?date={self.schedule1_org1.date}"
        response = self.client.get(filtered_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Оба расписания на эту дату
        self.assertEqual(len(response.data), 2)

    def test_schedule_filtering_by_teacher(self):
        """Тест фильтрации расписаний по преподавателю"""
        filtered_url = f"{self.list_url}?teacher={self.teacher1_org1.id}"
        response = self.client.get(filtered_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Только одно расписание с этим преподавателем
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.schedule1_org1.id)


class SubjectTests(BaseScheduleTestCase):
    """Тесты для предметов"""

    def setUp(self):
        super().setUp()
        
        self.list_url = reverse('subject-list')
        self.detail_url = reverse('subject-detail', kwargs={'pk': self.subject1_org1.pk})

    def test_get_subjects_list(self):
        """Тест получения списка предметов"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_subject_detail(self):
        """Тест получения деталей предмета"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.subject1_org1.id)
        self.assertEqual(response.data['name'], "Математика")

    def test_create_subject(self):
        """Тест создания предмета"""
        data = {
            'name': 'Биология'
        }
        
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subject.objects.filter(org=self.org1).count(), 3)

    def test_update_subject(self):
        """Тест обновления предмета"""
        data = {'name': 'Высшая математика'}
        
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.subject1_org1.refresh_from_db()
        self.assertEqual(self.subject1_org1.name, 'Высшая математика')

    def test_delete_subject(self):
        """Тест удаления предмета"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subject.objects.filter(org=self.org1).count(), 1)


class ClassroomTests(BaseScheduleTestCase):
    """Тесты для аудиторий"""

    def setUp(self):
        super().setUp()
        
        self.list_url = reverse('classroom-list')
        self.detail_url = reverse('classroom-detail', kwargs={'pk': self.classroom1_org1.pk})

    def test_get_classrooms_list(self):
        """Тест получения списка аудиторий"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_classroom_detail(self):
        """Тест получения деталей аудитории"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.classroom1_org1.id)
        self.assertEqual(response.data['title'], "101")

    def test_create_classroom(self):
        """Тест создания аудитории"""
        data = {
            'title': '103',
            'floor': 1,
            'building': 'Главный корпус'
        }
        
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Classroom.objects.filter(org=self.org1).count(), 3)

    def test_update_classroom(self):
        """Тест обновления аудитории"""
        data = {'title': '101А'}
        
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.classroom1_org1.refresh_from_db()
        self.assertEqual(self.classroom1_org1.title, '101А')

    def test_delete_classroom(self):
        """Тест удаления аудитории"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Classroom.objects.filter(org=self.org1).count(), 1)


class PeriodScheduleTests(BaseScheduleTestCase):
    """Тесты для периодических расписаний"""

    def setUp(self):
        super().setUp()
        
        # Создаем периодические расписания с отключенными сигналами
        self.period_schedule1_org1 = PeriodSchedule.objects.create(
            org=self.org1,
            title="Еженедельная математика",
            period=7,
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=self.teacher1_org1,
            classroom=self.classroom1_org1,
            group=self.group1_org1,
            subject=self.subject1_org1,
            lesson=1,
            start_date=date(2024, 1, 15),
            repeat_lessons_until_date=date(2024, 6, 15)
        )
        
        self.period_schedule1_org2 = PeriodSchedule.objects.create(
            org=self.org2,
            title="Еженедельная химия",
            period=7,
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=self.teacher1_org2,
            classroom=self.classroom1_org2,
            group=self.group1_org2,
            subject=self.subject1_org2,
            lesson=1,
            start_date=date(2024, 1, 15),
            repeat_lessons_until_date=date(2024, 6, 15)
        )
        
        self.list_url = reverse('period_schedule-list')
        self.detail_url = reverse('period_schedule-detail', kwargs={'pk': self.period_schedule1_org1.pk})

    def test_get_period_schedules_list(self):
        """Тест получения списка периодических расписаний"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Должны видеть только свои периодические расписания
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Еженедельная математика")

    def test_get_period_schedule_detail(self):
        """Тест получения деталей периодического расписания"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.period_schedule1_org1.id)
        self.assertEqual(response.data['title'], "Еженедельная математика")

    def test_create_period_schedule(self):
        """Тест создания периодического расписания"""
        data = {
            'title': 'Еженедельная физика',
            'period': 7,
            'start_time': '11:00:00',
            'end_time': '12:30:00',
            'teacher': self.teacher2_org1.id,
            'classroom': self.classroom2_org1.id,
            'group': self.group2_org1.id,
            'subject': self.subject2_org1.id,
            'lesson': 2,
            'start_date': '2024-01-16',
            'repeat_lessons_until_date': '2024-06-16'
        }
        
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PeriodSchedule.objects.filter(org=self.org1).count(), 2)

    def test_cannot_access_other_org_period_schedule(self):
        """Тест невозможности доступа к периодическому расписанию чужой организации"""
        url = reverse('period_schedule-detail', kwargs={'pk': self.period_schedule1_org2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AttendanceTests(BaseScheduleTestCase):
    """Тесты для посещений"""

    def setUp(self):
        super().setUp()
        
        # Создаем студентов с правильными полями
        self.student1_org1 = Student.objects.create(
            org=self.org1,
            first_name="Алексей",
            last_name="Студентов",
            student_group=self.group1_org1
        )
        
        self.student2_org1 = Student.objects.create(
            org=self.org1,
            first_name="Мария", 
            last_name="Студентова",
            student_group=self.group1_org1
        )
        
        # Создаем посещения
        self.attendance1_org1 = Attendance.objects.create(
            org=self.org1,
            student=self.student1_org1,
            lesson=self.schedule1_org1,
            was_present=True
        )
        
        self.attendance2_org1 = Attendance.objects.create(
            org=self.org1,
            student=self.student2_org1,
            lesson=self.schedule1_org1,
            was_present=False
        )
        
        self.list_url = reverse('attendance-list')
        self.detail_url = reverse('attendance-detail', kwargs={'pk': self.attendance1_org1.pk})

    def test_get_attendances_list(self):
        """Тест получения списка посещений"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_attendance_detail(self):
        """Тест получения деталей посещения"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.attendance1_org1.id)
        self.assertEqual(response.data['was_present'], True)

    def test_create_attendance(self):
        """Тест создания посещения"""
        # Создаем нового студента для теста
        new_student = Student.objects.create(
            org=self.org1,
            first_name="Новый",
            last_name="Студент",
            student_group=self.group1_org1
        )
        
        data = {
            'student': new_student.id,
            'lesson': self.schedule2_org1.id,
            'was_present': True
        }
        
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.filter(org=self.org1).count(), 3)

    def test_update_attendance(self):
        """Тест обновления посещения"""
        data = {'was_present': False}
        
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.attendance1_org1.refresh_from_db()
        self.assertEqual(self.attendance1_org1.was_present, False)


class GradeTests(BaseScheduleTestCase):
    """Тесты для оценок"""

    def setUp(self):
        super().setUp()
        
        # Создаем студентов с правильными полями
        self.student1_org1 = Student.objects.create(
            org=self.org1,
            first_name="Алексей",
            last_name="Студентов",
            student_group=self.group1_org1
        )
        
        # Создаем оценки
        self.grade1_org1 = Grade.objects.create(
            org=self.org1,
            student=self.student1_org1,
            lesson=self.schedule1_org1,
            value=5
        )
        
        self.grade2_org1 = Grade.objects.create(
            org=self.org1,
            student=self.student1_org1,
            lesson=self.schedule2_org1,
            value=4
        )
        
        self.list_url = reverse('grade-list')
        self.detail_url = reverse('grade-detail', kwargs={'pk': self.grade1_org1.pk})

    def test_get_grades_list(self):
        """Тест получения списка оценок"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_grade_detail(self):
        """Тест получения деталей оценки"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.grade1_org1.id)
        self.assertEqual(response.data['value'], 5)

    def test_create_grade(self):
        """Тест создания оценки"""
        # Создаем нового студента для теста
        new_student = Student.objects.create(
            org=self.org1,
            first_name="Новый",
            last_name="Студент",
            student_group=self.group1_org1
        )
        
        data = {
            'student': new_student.id,
            'lesson': self.schedule1_org1.id,
            'value': 3
        }
        
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Grade.objects.filter(org=self.org1).count(), 3)

    def test_update_grade(self):
        """Тест обновления оценки"""
        data = {'value': 2}
        
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.grade1_org1.refresh_from_db()
        self.assertEqual(self.grade1_org1.value, 2)

    def test_grade_unique_constraint(self):
        """Тест уникальности оценки для студента и урока"""
        data = {
            'student': self.student1_org1.id,
            'lesson': self.schedule1_org1.id,
            'value': 4
        }
        
        response = self.client.post(self.list_url, data, format='json')
        # Должна быть ошибка, т.к. оценка для этого студента и урока уже существует
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestScheduleTimeValidation(BaseScheduleTestCase):
    """Тесты для валидации времени в расписании"""

    def test_create_schedule_with_invalid_time(self):
        """Тест создания расписания с некорректным временем (конец раньше начала)"""
        data = {
            'title': 'Некорректный урок',
            'date': '2024-01-16',
            'start_time': '14:00:00',
            'end_time': '13:00:00',  # Конец раньше начала
            'teacher': self.teacher1_org1.id,
            'classroom': self.classroom1_org1.id,
            'group': self.group1_org1.id,
            'subject': self.subject1_org1.id
        }
        
        response = self.client.post(reverse('schedule-list'), data, format='json')
        # Должна быть ошибка валидации
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_schedule_with_overlapping_time(self):
        """Тест создания расписания с пересекающимся временем"""
        # Создаем расписание, которое пересекается по времени с существующим
        data = {
            'title': 'Пересекающийся урок',
            'date': '2024-01-15',  # Та же дата
            'start_time': '09:30:00',  # Начинается во время существующего урока
            'end_time': '11:00:00',
            'teacher': self.teacher1_org1.id,  # Тот же преподаватель
            'classroom': self.classroom1_org1.id,  # Та же аудитория
            'group': self.group1_org1.id,  # Та же группа
            'subject': self.subject1_org1.id
        }
        
        response = self.client.post(reverse('schedule-list'), data, format='json')
        # Должна быть ошибка валидации из-за пересечения
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)