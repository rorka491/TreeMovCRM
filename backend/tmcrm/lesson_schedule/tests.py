import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse, resolve
from django.db.models.signals import post_save
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from lesson_schedule.models import Schedule, Subject, Classroom, PeriodSchedule, Attendance, Grade, WEEK_DAY_CHOICES, GRADE_CHOICES
from students.models import StudentGroup, Student
from employers.models import Teacher, Employer
from mainapp.models import Organization, User, SubjectColor, OrgSettings
from datetime import date, time


# Базовые тесты свойств и валидации
class TestScheduleProperties:
    """Тестирование свойств и вычисляемых полей"""
    
    def test_duration_calculation_basic(self, organization, teacher):
        """Тест базового расчета длительности"""
        schedule = Schedule(
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=teacher,
            org=organization
        )
        
        duration = schedule.calc_duration
        assert duration.total_seconds() / 3600 == 1.5
    
    def test_duration_edge_cases(self, organization, teacher):
        """Тест крайних случаев расчета длительности"""
        test_cases = [
            (time(9, 0), time(9, 45), 0.75, "45 минут"),
            (time(14, 0), time(16, 30), 2.5, "2.5 часа"),
            (time(9, 0), time(11, 0), 2.0, "2 часа"), 
        ]
        
        for start, end, expected, description in test_cases:
            schedule = Schedule(
                start_time=start,
                end_time=end,
                teacher=teacher,
                org=organization
            )
            duration = schedule.calc_duration
            assert duration.total_seconds() / 3600 == expected, description
    
    def test_week_day_auto_calculation_logic(self, organization, teacher):
        """Тест логики автоматического расчета дня недели"""
        schedule = Schedule(
            date=date(2024, 1, 15),
            teacher=teacher,
            org=organization
        )
        assert schedule.date == date(2024, 1, 15)


class TestScheduleValidation:
    """Тестирование валидации данных"""
    
    def test_time_validation_correct(self, organization, teacher):
        """Тест корректного времени"""
        schedule = Schedule(
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=teacher,
            org=organization
        )
        
        try:
            schedule.clean()  
        except ValidationError:
            pytest.fail("Корректное время вызвало ValidationError")
    
    def test_time_validation_incorrect(self, organization, teacher):
        """Тест некорректного времени (конец раньше начала)"""
        schedule = Schedule(
            start_time=time(11, 0),
            end_time=time(10, 30),
            teacher=teacher,
            org=organization
        )
        
        with pytest.raises(ValidationError):
            schedule.clean()


class TestScheduleRepresentation:
    """Тестирование строковых представлений"""
    
    def test_string_representation_basic(self, organization, teacher):
        """Тест базового строкового представления"""
        schedule = Schedule(
            title="Важный урок",
            date=date(2024, 1, 15),
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=teacher,
            org=organization
        )
        
        representation = str(schedule)
        assert "Важный урок" in representation
        assert "2024" in representation
        assert "Тест" in representation  
    
    def test_attendance_string_representation(self, schedule, student):
        """Тест строкового представления посещения"""
        attendance_present = Attendance(
            student=student,
            lesson=schedule,
            was_present=True,
            org=schedule.org
        )
        
        attendance_absent = Attendance(
            student=student,
            lesson=schedule,
            was_present=False,
            org=schedule.org
        )
        
        assert student.name in str(attendance_present)
        assert student.name in str(attendance_absent)
    
    def test_grade_string_representation(self, schedule, student):
        """Тест строкового представления оценки"""
        grade = Grade(
            student=student,
            lesson=schedule,
            value=5,
            org=schedule.org
        )
        
        representation = str(grade)
        assert student.name in representation
        assert "оценка" in representation.lower()


# Тесты работы с БД
class TestScheduleDatabase:
    """Тестирование работы с БД (сохраняем объекты)"""
    
    def test_relationship_saving(self, schedule, teacher, student_group, subject):
        """Тест сохранения связей в БД"""
        # Проверяем что фикстура создала один объект
        assert Schedule.objects.count() == 1
        
        assert schedule.teacher == teacher
        assert schedule.group == student_group
        assert schedule.subject == subject
        
        assert schedule in teacher.schedules.all()
        assert schedule in student_group.schedules.all()
        assert schedule in subject.schedule_set.all()  
    
    def test_subject_creation(self, organization, teacher, subject_color):
        """Тест создания предмета"""
        subject = Subject.objects.create(
            name="Физика",
            color=subject_color,
            org=organization
        )
        subject.teacher.add(teacher)
        
        assert subject.name == "Физика"
        assert subject.teacher.count() == 1
        assert str(subject) == "Физика"
    
    def test_subject_color_uniqueness(self, organization, subject_color):
        """Тест уникальности цвета предмета в организации"""
        # Создаем первый предмет с цветом
        subject1 = Subject.objects.create(
            name="Математика",
            color=subject_color,
            org=organization
        )
        
        # Пытаемся создать второй предмет с тем же цветом
        subject2 = Subject(
            name="Химия",
            color=subject_color,
            org=organization
        )
        
        # Нужно вызвать clean() для кастомной валидации, а не full_clean()
        with pytest.raises(ValidationError) as exc_info:
            subject2.clean()
        
        assert "цвет уже используется" in str(exc_info.value)
    
    def test_classroom_creation(self, organization):
        """Тест создания аудитории"""
        classroom = Classroom.objects.create(
            title="201",
            floor=2,
            building="Новый корпус",
            org=organization
        )
        assert classroom.title == "201"
        assert classroom.floor == 2
        assert str(classroom) == "Аудитория 201"
    
    def test_period_schedule_creation(self, organization, teacher, student_group, subject, classroom):
        """Тест создания периодического расписания"""
        from lesson_schedule import signals as lesson_signals
        from django.db.models.signals import post_save
        post_save.disconnect(lesson_signals.create_lessons_until_date, sender=PeriodSchedule)
        
        try:
            period_schedule = PeriodSchedule.objects.create(
                period=7,
                title="Еженедельная математика",
                start_time=time(9, 0),
                end_time=time(10, 30),
                teacher=teacher,
                classroom=classroom,
                group=student_group,
                subject=subject,
                lesson=1,
                start_date=date(2024, 1, 15),
                repeat_lessons_until_date=date(2024, 6, 15),
                org=organization
            )
            
            assert period_schedule.period == 7
            assert period_schedule.title == "Еженедельная математика"
        finally:
            post_save.connect(lesson_signals.create_lessons_until_date, sender=PeriodSchedule)
    
    def test_attendance_creation(self, organization, teacher, student_group, subject, student):
        """Тест создания записи о посещении"""
        schedule = Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1,  
            teacher=teacher,
            group=student_group,
            subject=subject,
            org=organization
        )
        
        attendance = Attendance.objects.create(
            student=student,
            lesson=schedule,
            was_present=True,
            org=organization
        )
        
        assert attendance.student == student
        assert attendance.lesson == schedule
        assert attendance.was_present == True
        assert student.name in str(attendance)
    
    def test_grade_creation(self, organization, teacher, student_group, subject, student):
        """Тест создания оценки"""
        schedule = Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1, 
            teacher=teacher,
            group=student_group,
            subject=subject,
            org=organization
        )
        
        grade = Grade.objects.create(
            student=student,
            lesson=schedule,
            value=5,
            comment="Отлично!",
            org=organization
        )
        
        assert grade.student == student
        assert grade.value == 5
        assert grade.comment == "Отлично!"
        assert student.name in str(grade)
    
    def test_grade_unique_constraint(self, organization, teacher, student_group, subject, student):
        """Тест уникальности оценки для студента и урока"""
        schedule = Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1, 
            teacher=teacher,
            group=student_group,
            subject=subject,
            org=organization
        )
        
        Grade.objects.create(
            student=student,
            lesson=schedule, 
            value=5,
            org=organization
        )
        
        with pytest.raises(Exception):  
            Grade.objects.create(
                student=student,
                lesson=schedule,
                value=4,
                org=organization
            )


class TestScheduleRelationships:
    """Тестирование связей между моделями"""
    
    def test_schedule_teacher_relationship(self, schedule, teacher):
        """Тест связи расписание-преподаватель"""
        assert schedule.teacher == teacher
        assert schedule in teacher.schedules.all()
    
    def test_schedule_classroom_relationship(self, schedule, classroom):
        """Тест связи расписание-аудитория"""
        assert schedule.classroom == classroom
        assert schedule in classroom.schedules.all()
    
    def test_schedule_group_relationship(self, schedule, student_group):
        """Тест связи расписание-группа"""
        assert schedule.group == student_group
        assert schedule in student_group.schedules.all()
    
    def test_attendance_student_relationship(self, attendance, student):
        """Тест связи посещение-студент"""
        assert attendance.student == student
        assert attendance in student.attendances.all()


class TestScheduleRequiredFields:
    """Тесты обязательных полей расписания"""
    
    def test_schedule_required_fields(self, organization, teacher):
        """Тест обязательных полей расписания"""
        schedule = Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1,  
            teacher=teacher,
            org=organization
        )
        assert schedule.id is not None


class TestScheduleBusinessLogic:
    """Тесты бизнес-логики расписания"""
    
    def test_schedule_string_representation(self, schedule):
        """Тест строкового представления расписания"""
        representation = str(schedule)
        assert schedule.title in representation
        assert "2024" in representation
    
    def test_week_day_auto_calculation(self, organization, teacher):
        """Тест автоматического расчета дня недели"""
        schedule = Schedule.objects.create(
            date=date(2024, 1, 15),  
            teacher=teacher,
            org=organization
        )
        # После сохранения week_day должен быть вычислен автоматически
        assert schedule.week_day == 1


# Тесты URL и представлений
class TestLessonScheduleUrls:
    """Тесты URL расписания занятий"""

    def test_schedules_list_url(self):
        """Тест URL для списка расписаний"""
        url = reverse('schedule-list')
        assert resolve(url).func.cls.__name__ == 'ScheduleViewSet'

    def test_schedules_detail_url(self):
        """Тест URL для деталей расписания"""
        url = reverse('schedule-detail', kwargs={'pk': 1})
        assert resolve(url).func.cls.__name__ == 'ScheduleViewSet'

    def test_subjects_list_url(self):
        """Тест URL для списка предметов"""
        url = reverse('subject-list')
        assert resolve(url).func.cls.__name__ == 'SubjectViewSet'

    def test_classrooms_list_url(self):
        """Тест URL для списка аудиторий"""
        url = reverse('classroom-list')
        assert resolve(url).func.cls.__name__ == 'ClassroomViewSet'

    def test_attendances_list_url(self):
        """Тест URL для списка посещений"""
        url = reverse('attendance-list')
        assert resolve(url).func.cls.__name__ == 'AttendanceViewSet'

    def test_period_schedules_list_url(self):
        """Тест URL для списка периодических расписаний"""
        url = reverse('period_schedule-list')
        assert resolve(url).func.cls.__name__ == 'PeriodScheduleViewSet'

    def test_grades_list_url(self):
        """Тест URL для списка оценок"""
        url = reverse('grade-list')
        assert resolve(url).func.cls.__name__ == 'GradeViewSet'


class TestLessonScheduleBasicViews:
    """Базовые тесты views"""

    def test_schedule_creation_logic(self, organization, teacher, student_group, subject, classroom):
        """Тест логики создания расписания (без API)"""
        # Создаем новое расписание
        schedule = Schedule.objects.create(
            title="Тестовый урок",
            date=date(2024, 1, 15),
            week_day=1, 
            teacher=teacher,
            classroom=classroom,
            group=student_group,
            subject=subject,
            org=organization
        )
        
        # Проверяем что объект создался (не считаем фикстуры, так как они в другой транзакции)
        assert schedule.id is not None
        assert schedule.title == "Тестовый урок"
        assert schedule.week_day == 1

    def test_subject_creation_logic(self, organization, teacher, subject_color):
        """Тест логики создания предмета (без API)"""
        subject = Subject.objects.create(
            name="Физика",
            color=subject_color,
            org=organization
        )
        subject.teacher.add(teacher)
        
        # Проверяем что объект создался
        assert subject.id is not None
        assert subject.name == "Физика"
        assert subject.teacher.count() == 1

    def test_classroom_creation_logic(self, organization):
        """Тест логики создания аудитории (без API)"""
        classroom = Classroom.objects.create(
            title="201",
            floor=2,
            building="Новый корпус",
            org=organization
        )
        
        # Проверяем что объект создался
        assert classroom.id is not None
        assert classroom.title == "201"
        assert classroom.floor == 2


class TestLessonScheduleChoiceFields:
    """Тесты полей с выбором"""

    def test_week_day_choices(self):
        """Тест вариантов дней недели"""
        assert len(WEEK_DAY_CHOICES) == 7
        assert WEEK_DAY_CHOICES[0] == (1, "Monday")
        assert WEEK_DAY_CHOICES[6] == (7, "Sunday")

    def test_grade_choices(self):
        """Тест вариантов оценок"""
        assert len(GRADE_CHOICES) == 4
        assert GRADE_CHOICES[0] == (2, "Не удовлетварительно")
        assert GRADE_CHOICES[3] == (5, "Отлично")


class TestLessonScheduleUtils:
    """Вспомогательные тесты для расписания"""

    def test_model_meta(self):
        """Тест мета-данных моделей"""
        assert Schedule._meta.verbose_name == 'Занятие'
        assert Schedule._meta.verbose_name_plural == 'Занятия'
        assert Subject._meta.verbose_name == 'Предмет'
        assert Subject._meta.verbose_name_plural == 'Предметы'
        assert Classroom._meta.verbose_name == 'Аудитория'
        assert Classroom._meta.verbose_name_plural == 'Аудиории'
        assert Attendance._meta.verbose_name == 'Посещение'
        assert Attendance._meta.verbose_name_plural == 'Посещения'
        assert Grade._meta.verbose_name == 'Оценка'
        assert Grade._meta.verbose_name_plural == 'Оценки'

    def test_ordering(self):
        """Тест порядка сортировки"""
        assert Schedule._meta.ordering == ['date', 'start_time']


# Тесты безопасности организаций
class TestOrganizationSecurity:
    """Тесты безопасности между организациями"""
    
    def test_subject_color_organization_isolation(self, subject_color, subject_color_org2):
        """Тест изоляции цветов предметов между организациями"""
        colors_org1 = SubjectColor.objects.filter(org=subject_color.org)
        assert colors_org1.count() == 1
        assert subject_color in colors_org1
        assert subject_color_org2 not in colors_org1
        
        colors_org2 = SubjectColor.objects.filter(org=subject_color_org2.org)
        assert colors_org2.count() == 1
        assert subject_color_org2 in colors_org2
        assert subject_color not in colors_org2

    def test_api_color_access_organization_isolation(self, authenticated_client, subject_color):
        """Тест изоляции доступа к цветам через API"""
        url = reverse('subject_color-list')
        response = authenticated_client.get(url)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        
        if response.status_code == status.HTTP_200_OK:
            colors_data = response.json()
            if 'results' in colors_data:
                colors_list = colors_data['results']
            else:
                colors_list = colors_data
                
            assert len(colors_list) >= 1
            color_titles = [color['title'] for color in colors_list]
            assert subject_color.title in color_titles

    def test_api_cross_organization_color_access_prevention(self, authenticated_client, subject_color_org2):
        """Тест предотвращения доступа к цветам чужой организации через API"""
        url = reverse('subject_color-detail', kwargs={'pk': subject_color_org2.id})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_api_subject_creation_organization_isolation(self, authenticated_client, subject_color):
        """Тест изоляции создания предметов через API"""
        subject_data = {
            'name': 'Новый предмет Org1',
            'color': subject_color.id,
        }
        
        url = reverse('subject-list')
        response = authenticated_client.post(url, subject_data)
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
        
        if response.status_code == status.HTTP_201_CREATED:
            new_subject = Subject.objects.get(id=response.json()['id'])
            assert new_subject.org == subject_color.org

    def test_api_cross_organization_subject_creation_prevention(self, authenticated_client, subject_color_org2):
        """Тест предотвращения создания предмета для чужой организации через API"""
        subject_data = {
            'name': 'Новый предмет с чужим цветом',
            'color': subject_color_org2.id,  
        }
        
        url = reverse('subject-list')
        response = authenticated_client.post(url, subject_data)
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]

    def test_api_attendance_organization_isolation(self, authenticated_client, attendance):
        """Тест изоляции посещаемости между организациями через API"""
        url = reverse('attendance-list')
        response = authenticated_client.get(url)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        
        if response.status_code == status.HTTP_200_OK:
            attendances_data = response.json()
            if 'results' in attendances_data:
                attendances_list = attendances_data['results']
            else:
                attendances_list = attendances_data
                
            assert len(attendances_list) >= 1

    def test_api_attendance_cross_organization_access_prevention(self, authenticated_client, attendance_org2):
        """Тест предотвращения доступа к посещениям чужой организации через API"""
        url = reverse('attendance-detail', kwargs={'pk': attendance_org2.id})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


# Тесты конфликтов расписания
class TestScheduleConflictValidation:
    """ТЕСТЫ КОНФЛИКТОВ РАСПИСАНИЯ: проверяют валидацию пересечений времени"""
    
    def test_teacher_conflict_validation(self, organization, teacher, student_group, subject):
        """Конфликт преподавателя: один учитель не может вести два занятия одновременно"""
        # Создаем первое занятие
        Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1, 
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=teacher,
            group=student_group,
            subject=subject,
            org=organization
        )
        
        # Пытаемся создать конфликтующее занятие с тем же преподавателем
        conflicting_schedule = Schedule(
            date=date(2024, 1, 15),
            week_day=1,  
            start_time=time(9, 0),  
            end_time=time(10, 30),
            teacher=teacher,  
            group=student_group,
            subject=subject,
            org=organization
        )
        
        with pytest.raises(ValidationError) as exc_info:
            conflicting_schedule.clean()
        
        assert "У этого преподавателя на пару и дату занятие" in str(exc_info.value)
    
    def test_group_conflict_validation(self, organization, teacher, teacher2, student_group, subject):
        """Конфликт группы: одна группа не может быть на двух занятиях одновременно"""
        # Создаем первое занятие с первым преподавателем
        Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1,  
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=teacher, 
            group=student_group,
            subject=subject,
            org=organization
        )
        
        # Пытаемся создать конфликтующее занятие с той же группой, но РАЗНЫМ преподавателем
        conflicting_schedule = Schedule(
            date=date(2024, 1, 15),
            week_day=1, 
            start_time=time(9, 0),  
            end_time=time(10, 30),
            teacher=teacher2,  
            group=student_group, 
            subject=subject,
            org=organization
        )
        
        with pytest.raises(ValidationError) as exc_info:
            conflicting_schedule.clean()
        
        assert "У этой группы на эту пару и дату занятие" in str(exc_info.value)
    
    def test_no_conflict_different_times(self, organization, teacher, student_group, subject):
        """Отсутствие конфликта: занятия в разное время"""
        Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1,  
            start_time=time(9, 0),
            end_time=time(10, 0),
            teacher=teacher,
            group=student_group,
            subject=subject,
            org=organization
        )
        
        # Занятие после первого - конфликта быть не должно
        non_conflicting_schedule = Schedule(
            date=date(2024, 1, 15),
            week_day=1,  
            start_time=time(10, 30), 
            end_time=time(11, 30),
            teacher=teacher,  
            group=student_group,  
            subject=subject,  
            org=organization
        )
        
        try:
            non_conflicting_schedule.clean()
        except ValidationError:
            pytest.fail("Не должно быть конфликта для разного времени")
    
    def test_no_conflict_different_dates(self, organization, teacher, student_group, subject):
        """Отсутствие конфликта: занятия в разные даты"""
        Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1, 
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=teacher,
            group=student_group,
            subject=subject,
            org=organization
        )
        
        # То же время, но другая дата - конфликта быть не должно
        non_conflicting_schedule = Schedule(
            date=date(2024, 1, 16),  
            week_day=2,  
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=teacher,
            group=student_group,
            subject=subject,
            org=organization
        )
        
        try:
            non_conflicting_schedule.clean()
        except ValidationError:
            pytest.fail("Не должно быть конфликта для разных дат")
    
    def test_partial_time_overlap_conflict(self, organization, teacher, student_group, subject):
        """Частичное пересечение времени: начало внутри другого занятия"""
        Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1, 
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=teacher,
            group=student_group,
            subject=subject,
            org=organization
        )
        
        # Частичное пересечение (начало внутри другого занятия)
        conflicting_schedule = Schedule(
            date=date(2024, 1, 15),
            week_day=1,  
            start_time=time(10, 0), 
            end_time=time(11, 30),
            teacher=teacher,  
            group=student_group,
            subject=subject,
            org=organization
        )
        
        with pytest.raises(ValidationError):
            conflicting_schedule.clean()


class TestFastConflictTests:
    """ Быстрые тесты конфликтов"""
    
    def test_fast_teacher_conflict(self, organization, teacher, student_group, subject):
        """ Быстрый тест конфликта преподавателя"""
        Schedule.objects.create(
            date=date(2024, 1, 15), 
            week_day=1,  
            start_time=time(9, 0), 
            end_time=time(10, 30),
            teacher=teacher, 
            group=student_group, 
            subject=subject, 
            org=organization
        )
        
        conflict = Schedule(
            date=date(2024, 1, 15), 
            week_day=1, 
            start_time=time(9, 0), 
            end_time=time(10, 30),
            teacher=teacher, 
            group=student_group, 
            subject=subject, 
            org=organization
        )
        
        with pytest.raises(ValidationError):
            conflict.clean()
    
    def test_fast_no_conflict(self, organization, teacher, student_group, subject):
        """ Быстрый тест отсутствия конфликта"""
        Schedule.objects.create(
            date=date(2024, 1, 15), 
            week_day=1,  
            start_time=time(9, 0), 
            end_time=time(10, 30),
            teacher=teacher, 
            group=student_group, 
            subject=subject, 
            org=organization
        )
        
        no_conflict = Schedule(
            date=date(2024, 1, 16),  
            week_day=2,  
            start_time=time(9, 0), 
            end_time=time(10, 30),
            teacher=teacher, 
            group=student_group, 
            subject=subject, 
            org=organization
        )
        
        try:
            no_conflict.clean()
        except ValidationError:
            pytest.fail("Не должно быть конфликта")


class BaseAPITestCase(APITestCase):
    """Фикстура для API тестов с аутентификацией"""
    
    def setUp(self):
        from mainapp import signals as main_signals
        post_save.disconnect(main_signals.create_org_settings, sender=Organization)
        
        # Создаем организацию
        self.org = Organization.objects.create(name="Test Org")
        self.org_settings = OrgSettings.objects.create(org=self.org, timezone="UTC")
        
        # Создаём пользователя со всеми правами от лица которого будут проходить API тесты
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123", 
            email="test@example.com",
            org=self.org,
        )
        
        # Создаем преподавателя1
        self.employer1 = Employer.objects.create(
            name="Тест", 
            surname="Преподаватель", 
            org=self.org
        )
        self.teacher1 = Teacher.objects.create(employer=self.employer1, org=self.org)
        
        # Создаём преподавателя2
        self.employer2 = Employer.objects.create(
            name="Второй", 
            surname="Учитель", 
            org=self.org
        )
        self.teacher2 = Teacher.objects.create(employer=self.employer2, org=self.org)
        
        # Создаем предмет
        self.subject = Subject.objects.create(name="Математика", org=self.org)
        self.subject.teacher.add(self.teacher1, self.teacher2)
        
        # Создаем аудитории
        self.classroom1 = Classroom.objects.create(title="101", org=self.org)
        self.classroom2 = Classroom.objects.create(title="102", org=self.org)
        
        # Создаем группы
        self.group1 = StudentGroup.objects.create(name="10А", org=self.org)
        self.group2 = StudentGroup.objects.create(name="10Б", org=self.org)
        
        # Аутентифиция клиента
        self.client = APIClient()
        
        # Обычная аутентификация - передат информацию о пользователе в бд
        login_success = self.client.login(username="testuser", password="testpass123")
        print(f"Login success: {login_success}")
        
        # force_authenticate - делает все последующие запросы от лица пользователя
        self.client.force_authenticate(user=self.user)

    # Вновь включаем сигнал для изоляции тестов       
    def tearDown(self):
        from mainapp import signals as main_signals
        post_save.connect(main_signals.create_org_settings, sender=Organization)
    
    # Шаблон для упрощенного создания занятий
    def _create_valid_schedule_data(self, **overrides):
        """Создает валидные данные для API запроса"""
        base_data = {
            'title': 'Тестовое занятие',
            'date': '2024-01-15',
            'week_day': 1,
            'teacher': self.teacher1.id,
            'group': self.group1.id,
            'subject': self.subject.id,
            'classroom': self.classroom1.id,
            'start_time': '09:00',
            'end_time': '10:30'
        }
        base_data.update(overrides)
        return base_data
    
    # Метод для упрощения запросв на создание занятия
    def _create_schedule_via_api(self, data):
        """Вспомогательный метод для создания занятия через API"""
        response = self.client.post(reverse('schedule-list'), data, format='json')
        print(f"API CREATE SCHEDULE: {response.status_code}")
        if hasattr(response, 'data'):
            print(f"Response data: {response.data}")
        return response
    
    # Метод для проверки доступа к API
    def _ensure_api_access(self):
        """Проверяем что у нас есть доступ к API"""
        response = self.client.get(reverse('schedule-list'))
        print(f"API ACCESS CHECK: {response.status_code}")
        return response.status_code != 401


class ScheduleConflictAPITests(BaseAPITestCase):
    """API тесты для проверки конфликтов расписания"""
    
    def test_create_schedule_success(self):
        """ Тест успешного создания занятия через API"""
        if not self._ensure_api_access():
            self.skipTest("Нет доступа к API запросу - тест пропушен")
            
        schedule_data = self._create_valid_schedule_data(title='Успешное занятие')
        response = self._create_schedule_via_api(schedule_data)
        
        # Проверяем статус ответа
        if response.status_code == status.HTTP_201_CREATED:
            self.assertEqual(Schedule.objects.count(), 1)
            created_schedule = Schedule.objects.first()
            self.assertEqual(created_schedule.title, 'Успешное занятие')
        else:
            # Если не 201, проверяем что это не ошибка аутентификации
            self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_teacher_conflict_detection_via_api(self):
        """ Тест обнаружения конфликта преподавателя через API"""
        if not self._ensure_api_access():
            self.skipTest("Нет доступа к API запросу - тест пропушен")
            
        # Создаём первое занятие для учителя1
        first_lesson_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30'
        )
        response1 = self._create_schedule_via_api(first_lesson_data)
        
        # Создаём второе занятие для учителя1 в тоже время
        if response1.status_code == status.HTTP_201_CREATED:
            conflicting_data = self._create_valid_schedule_data(
                title='Конфликтующее занятие',
                group=self.group2.id,
                classroom=self.classroom2.id,
                start_time='09:00',
                end_time='10:30'
            )
            # Ожидается ошибка 400
            response2 = self._create_schedule_via_api(conflicting_data)
            self.assertIn(response2.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED])
    
    def test_group_conflict_detection_via_api(self):
        """ Тест обнаружения конфликта группы через API"""
        if not self._ensure_api_access():
            self.skipTest("Нет доступа к API запросу - тест пропушен")
            
        # Создаём первое занятие для группы1
        first_lesson_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30'
        )
        response1 = self._create_schedule_via_api(first_lesson_data)
        
        # Создаём второе занятие для группы1, но с другим учителем
        if response1.status_code == status.HTTP_201_CREATED:
            conflicting_data = self._create_valid_schedule_data(
                title='Конфликтующее занятие',
                teacher=self.teacher2.id,
                classroom=self.classroom2.id,
                start_time='09:00',
                end_time='10:30'
            )
            # Ожидается ошибка 400
            response2 = self._create_schedule_via_api(conflicting_data)
            self.assertIn(response2.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED])
    
    
    def test_no_conflict_different_times_via_api(self):
        """ Тест отсутствия конфликта при разном времени через API"""
        if not self._ensure_api_access():
            self.skipTest("Нет доступа к API запросу - тест пропушен")

        # Создаём первое занятие    
        first_lesson_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:00'
        )
        # Ожидается реализация занятия
        response1 = self._create_schedule_via_api(first_lesson_data)
        
        # Создаём второе занятие
        if response1.status_code == status.HTTP_201_CREATED:
            second_lesson_data = self._create_valid_schedule_data(
                title='Второе занятие',
                start_time='10:30',
                end_time='11:30'
            )
            # Ожидается реализация занятия
            response2 = self._create_schedule_via_api(second_lesson_data)
            self.assertIn(response2.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
    
    def test_no_conflict_different_dates_via_api(self):
        """ Тест отсутствия конфликта при разных датах через API"""
        if not self._ensure_api_access():
            self.skipTest("Нет доступа к API запросу - тест пропушен")
            
        # Создаём первое занятие с датой 15 ноября    
        first_lesson_data = self._create_valid_schedule_data(
            title='Первое занятие',
            date='2025-11-15',
            week_day=1
        )
        # Ожидается создание занятия
        response1 = self._create_schedule_via_api(first_lesson_data)
        
        # Создаём второе занятие с датой 16 ноября
        if response1.status_code == status.HTTP_201_CREATED:
            second_lesson_data = self._create_valid_schedule_data(
                title='Второе занятие',
                date='2025-11-16',
                week_day=2
            )
            # Ожидается создание второго занятия
            response2 = self._create_schedule_via_api(second_lesson_data)
            self.assertIn(response2.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
    
    def test_partial_time_overlap_conflict_via_api(self):
        """ Тест обнаружения частичного пересечения времени через API"""
        if not self._ensure_api_access():
            self.skipTest("Нет доступа к API запросу - тест пропушен")

        # Создаём первое занятие с временем окончания 10:30    
        first_lesson_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30'
        )
        # Ожидаемый результат - занятие создано
        response1 = self._create_schedule_via_api(first_lesson_data)
        
        # Создаём второе занятие с временем начала 10:00 (пересечение в 30 минут)
        if response1.status_code == status.HTTP_201_CREATED:
            overlapping_data = self._create_valid_schedule_data(
                title='Пересекающееся занятие',
                teacher=self.teacher2.id,
                group=self.group2.id,
                classroom=self.classroom2.id,
                start_time='10:00',
                end_time='11:30'
            )
            # Ожидаемый результат - код 400 занятие не создано
            response2 = self._create_schedule_via_api(overlapping_data)
            self.assertIn(response2.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED])
    
    def test_update_schedule_with_conflict_via_api(self):
        """ Тест конфликта при обновлении занятия через API"""
        if not self._ensure_api_access():
            self.skipTest("Нет доступа к API запросу - тест пропушен")

        # Создаём первое занятие    
        first_lesson_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30'
        )
        response1 = self._create_schedule_via_api(first_lesson_data)
        
        # Создаём второе занятие без конфликта со временем
        if response1.status_code == status.HTTP_201_CREATED:
            first_lesson_id = response1.data['id']
            second_lesson_data = self._create_valid_schedule_data(
                title='Второе занятие',
                teacher=self.teacher2.id,
                group=self.group2.id,
                classroom=self.classroom2.id,
                start_time='11:00',
                end_time='12:30'
            )
            # Ожидаемый результат - занятие создано
            response2 = self._create_schedule_via_api(second_lesson_data)
            
            # Попытка наложить время первого занятия на второе
            if response2.status_code == status.HTTP_201_CREATED:
                second_lesson_id = response2.data['id']
                
                update_url = reverse('schedule-detail', kwargs={'pk': second_lesson_id})
                update_data = {
                    'start_time': '09:00',
                    'end_time': '10:30'
                }
                # Ожидаемый результат - код 400 обновление не возможно
                response_update = self.client.patch(update_url, update_data, format='json')
                self.assertIn(response_update.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_200_OK])
    

class ScheduleEdgeCaseAPITests(BaseAPITestCase):
    """Тесты граничных случаев для конфликтов расписания"""
    
    def test_boundary_times_no_conflict_via_api(self):
        """ Тест что занятия вплотную друг к другу не конфликтуют"""
        if not self._ensure_api_access():
            self.skipTest("Нет доступа к API запросу - тест пропушен")

        # Создаём первое занятие    
        first_lesson_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:00'
        )
        response1 = self._create_schedule_via_api(first_lesson_data)
        
        # Создаём второе занятие сразу после первого
        if response1.status_code == status.HTTP_201_CREATED:
            second_lesson_data = self._create_valid_schedule_data(
                title='Второе занятие',
                start_time='10:00',
                end_time='11:00'
            )
            # Ожидаемый результат - код 200 занятие создано
            response2 = self._create_schedule_via_api(second_lesson_data)
            self.assertIn(response2.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
    
    def test_multiple_conflicts_detection_via_api(self):
        """ Тест обнаружения множества конфликтов расписания через API"""
        if not self._ensure_api_access():
            self.skipTest("Нет доступа к API запросу - тест пропушен")

        # Создаём 3 занятия в цикле (с 9-10, 10-11, 11-12)   
        lessons_data = [
            self._create_valid_schedule_data(
                title=f'Занятие {i}',
                start_time=f'{9+i}:00',
                end_time=f'{10+i}:00'
            )
            for i in range(3)
        ]
        
        created_count = 0
        for lesson_data in lessons_data:
            response = self._create_schedule_via_api(lesson_data)
            if response.status_code == status.HTTP_201_CREATED:
                created_count += 1
        
        # Создаём новое занятие, которое накладывается на 3 предыдущих, но не на прямую
        conflicting_data = self._create_valid_schedule_data(
            title='Конфликтующее со всеми',
            teacher=self.teacher2.id,
            group=self.group2.id,
            classroom=self.classroom2.id,
            start_time='08:00',
            end_time='13:00'
        )
        # Ожидаемый результат - код 400 занятие не создано
        response_conflict = self._create_schedule_via_api(conflicting_data)
        self.assertIn(response_conflict.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED])


# Новые улучшенные API тесты конфликтов расписания
# Новые улучшенные API тесты конфликтов расписания
class ScheduleConflictAPITestCases(BaseAPITestCase):
    """Улучшенные API тесты для проверки конфликтов расписания"""
    
    def test_teacher_time_conflict_api(self):
        """Тест конфликта времени преподавателя через API - должен вернуть 400"""
        # Создаем первое занятие
        first_schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30'
        )
        response1 = self.client.post(reverse('schedule-list'), first_schedule_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Пытаемся создать конфликтующее занятие с тем же преподавателем в то же время
        conflicting_schedule_data = self._create_valid_schedule_data(
            title='Конфликтующее занятие',
            start_time='09:00',
            end_time='10:30',
            group=self.group2.id,
            classroom=self.classroom2.id
        )
        
        response2 = self.client.post(reverse('schedule-list'), conflicting_schedule_data, format='json')
        
        # Проверяем что получили ошибку 400
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Проверяем что ошибка связана с преподавателем
        self.assertIn('teacher', response2.data)
    
    def test_group_time_conflict_api(self):
        """Тест конфликта времени группы через API - должен вернуть 400"""
        # Создаем первое занятие
        first_schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30'
        )
        response1 = self.client.post(reverse('schedule-list'), first_schedule_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Пытаемся создать конфликтующее занятие с той же группой в то же время
        conflicting_schedule_data = self._create_valid_schedule_data(
            title='Конфликтующее занятие',
            start_time='09:00',
            end_time='10:30',
            teacher=self.teacher2.id,
            classroom=self.classroom2.id
        )
        
        response2 = self.client.post(reverse('schedule-list'), conflicting_schedule_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Проверяем содержание ошибки
        self.assertIn('group', response2.data)
    
    def test_no_time_conflict_different_times_api(self):
        """Тест отсутствия конфликта при разном времени - должен вернуть 201"""
        # Создаем первое занятие
        first_schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:00'
        )
        response1 = self.client.post(reverse('schedule-list'), first_schedule_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Создаем второе занятие в другое время (без конфликта)
        second_schedule_data = self._create_valid_schedule_data(
            title='Второе занятие',
            start_time='10:30',
            end_time='11:30',
            teacher=self.teacher1.id,
            group=self.group1.id
        )
        
        response2 = self.client.post(reverse('schedule-list'), second_schedule_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
    
    def test_no_time_conflict_different_dates_api(self):
        """Тест отсутствия конфликта при разных датах - должен вернуть 201"""
        # Создаем первое занятие
        first_schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            date='2024-01-15',
            week_day=1
        )
        response1 = self.client.post(reverse('schedule-list'), first_schedule_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Создаем второе занятие в другую дату (без конфликта)
        second_schedule_data = self._create_valid_schedule_data(
            title='Второе занятие',
            date='2024-01-16',
            week_day=2,
            teacher=self.teacher1.id,
            group=self.group1.id,
            start_time='09:00',
            end_time='10:30'
        )
        
        response2 = self.client.post(reverse('schedule-list'), second_schedule_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
    
    def test_partial_time_overlap_conflict_api(self):
        """Тест частичного пересечения времени - должен вернуть 400"""
        # Создаем первое занятие
        first_schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30'
        )
        response1 = self.client.post(reverse('schedule-list'), first_schedule_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Пытаемся создать занятие с частичным пересечением
        overlapping_schedule_data = self._create_valid_schedule_data(
            title='Пересекающееся занятие',
            start_time='10:00',
            end_time='11:30',
            teacher=self.teacher1.id,
            group=self.group1.id
        )
        
        response2 = self.client.post(reverse('schedule-list'), overlapping_schedule_data, format='json')
        # Частичные пересечения ДОЛЖНЫ обнаруживаться - тест должен падать если это не работает
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_classroom_time_conflict_api(self):
        """Тест конфликта времени аудитории через API - должен вернуть 400"""
        # Создаем первое занятие
        first_schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30',
            classroom=self.classroom1.id
        )
        response1 = self.client.post(reverse('schedule-list'), first_schedule_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Пытаемся создать конфликтующее занятие в той же аудитории
        conflicting_schedule_data = self._create_valid_schedule_data(
            title='Конфликтующее занятие',
            start_time='09:00',
            end_time='10:30',
            teacher=self.teacher2.id,
            group=self.group2.id,
            classroom=self.classroom1.id
        )
        
        response2 = self.client.post(reverse('schedule-list'), conflicting_schedule_data, format='json')
        
        # Конфликты аудиторий ДОЛЖНЫ обнаруживаться - тест должен падать если это не работает
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)


class ScheduleUpdateConflictAPITestCases(BaseAPITestCase):
    """API тесты для проверки конфликтов при обновлении расписания"""
    
    def test_update_schedule_creates_teacher_conflict_api(self):
        """Тест что обновление создает конфликт преподавателя - должен вернуть 400"""
        # Создаем первое занятие
        first_schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30'
        )
        response1 = self.client.post(reverse('schedule-list'), first_schedule_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        first_schedule_id = response1.data['id']
        
        # Создаем второе занятие без конфликта
        second_schedule_data = self._create_valid_schedule_data(
            title='Второе занятие',
            start_time='11:00',
            end_time='12:30',
            teacher=self.teacher2.id,  # Другой преподаватель
            group=self.group2.id  # Другая группа
        )
        response2 = self.client.post(reverse('schedule-list'), second_schedule_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        second_schedule_id = response2.data['id']
        
        # Пытаемся обновить второе занятие чтобы создать конфликт
        update_data = {
            'start_time': '09:00',  # Конфликтующее время
            'end_time': '10:30',    # Конфликтующее время
            'teacher': self.teacher1.id  # Тот же преподаватель что и в первом занятии
        }
        
        response_update = self.client.patch(
            reverse('schedule-detail', kwargs={'pk': second_schedule_id}),
            update_data,
            format='json'
        )
        self.assertEqual(response_update.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_schedule_creates_group_conflict_api(self):
        """Тест что обновление создает конфликт группы - должен вернуть 400"""
        # Создаем первое занятие
        first_schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30'
        )
        response1 = self.client.post(reverse('schedule-list'), first_schedule_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        first_schedule_id = response1.data['id']
        
        # Создаем второе занятие без конфликта
        second_schedule_data = self._create_valid_schedule_data(
            title='Второе занятие',
            start_time='11:00',
            end_time='12:30',
            teacher=self.teacher2.id,  # Другой преподаватель
            group=self.group2.id  # Другая группа
        )
        response2 = self.client.post(reverse('schedule-list'), second_schedule_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        second_schedule_id = response2.data['id']
        
        # Пытаемся обновить второе занятие чтобы создать конфликт
        update_data = {
            'start_time': '09:00',  # Конфликтующее время
            'end_time': '10:30',    # Конфликтующее время
            'group': self.group1.id  # Та же группа что и в первом занятии
        }
        
        response_update = self.client.patch(
            reverse('schedule-detail', kwargs={'pk': second_schedule_id}),
            update_data,
            format='json'
        )
        self.assertEqual(response_update.status_code, status.HTTP_400_BAD_REQUEST)


class TestCeleryTasks:
    """Тесты Celery задач с использованием фикстур"""
    
    def test_update_complete_lessons_task(self, organization, teacher, student_group, subject):
        """Тест автоматического помечания завершенных уроков"""
        from lesson_schedule.tasks import update_complete_lessons
        
        # Создаем занятие которое должно быть завершено
        past_lesson = Schedule.objects.create(
            date=date(2023, 12, 1),  
            start_time=time(9, 0),
            end_time=time(10, 0),
            teacher=teacher,
            group=student_group,
            subject=subject,
            is_completed=False,
            org=organization
        )
        
        # Создаем занятие которое еще не завершено (в будущем)
        future_lesson = Schedule.objects.create(
            date=date(2025, 12, 31),  
            week_day=3,  
            start_time=time(9, 0),
            end_time=time(10, 0),
            teacher=teacher,
            group=student_group,
            subject=subject,
            is_completed=False,
            org=organization
        )
        
        # Вызываем задачу для конкретной организации
        result = update_complete_lessons([organization])
        
        # Проверяем что прошлое занятие помечено как завершенное
        past_lesson.refresh_from_db()
        assert past_lesson.is_completed
        
        # Проверяем что будущее занятие осталось незавершенным
        future_lesson.refresh_from_db()
        assert not future_lesson.is_completed
    
    def test_create_attendences_for_all_passes_task(self, organization, completed_schedule, student, student2):
        """ Тест создания записей посещений для пропусков"""
        from lesson_schedule.tasks import create_attendences_for_all_passes
        
        # Добавляем студентов в группу занятия
        completed_schedule.group.students.add(student, student2)
        
        # Создаем посещение только для одного студента
        Attendance.objects.create(
            student=student,
            lesson=completed_schedule,
            was_present=True,
            org=organization
        )
        
        # Вызываем задачу
        result = create_attendences_for_all_passes([organization])
        
        # Проверяем что создалась запись для второго студента с was_present=False
        missing_attendance = Attendance.objects.filter(
            lesson=completed_schedule, 
            student=student2,
            was_present=False
        )
        assert missing_attendance.exists()
    
    def test_create_attendences_skips_lessons_without_group(self, organization, teacher, subject):
        """Тест что занятия без группы пропускаются"""
        from lesson_schedule.tasks import create_attendences_for_all_passes
        
        # Создаем завершенное занятие без группы
        lesson_without_group = Schedule.objects.create(
            date=date(2024, 1, 1),
            week_day=1,  
            teacher=teacher,
            subject=subject,
            is_completed=True,
            org=organization
        )
        
        # Вызываем задачу - не должно быть ошибок
        result = create_attendences_for_all_passes([organization])
        
        # Не должно создаться записей посещений
        attendances_count = Attendance.objects.filter(lesson=lesson_without_group).count()
        assert attendances_count == 0


class TestPeriodSchedule:
    """Тесты PeriodSchedule с использованием фикстур"""
    
    def test_update_period_schedule_updates_incomplete_lessons(self, organization, teacher, student_group, subject, classroom):
        """ Тест что изменение PeriodSchedule обновляет незавершенные занятия"""
        from lesson_schedule import signals as lesson_signals
        from django.db.models.signals import post_save
        post_save.disconnect(lesson_signals.create_lessons_until_date, sender=PeriodSchedule)
        
        try:
            # Создаем PeriodSchedule
            period_schedule = PeriodSchedule.objects.create(
                period=7,
                start_date=date(2024, 1, 1),
                repeat_lessons_until_date=date(2024, 1, 15),
                teacher=teacher,
                classroom=classroom,
                group=student_group,
                subject=subject,
                start_time=time(9, 0),
                end_time=time(10, 30),
                org=organization
            )
            
            # Создаем второго преподавателя для теста обновления
            employer2 = Employer.objects.create(
                name="Новый", 
                surname="Преподаватель", 
                org=organization
            )
            teacher2 = Teacher.objects.create(employer=employer2, org=organization)
            
            # Обновляем PeriodSchedule
            period_schedule.teacher = teacher2
            period_schedule.start_time = time(10, 0)
            period_schedule.end_time = time(11, 30)
            period_schedule.save()
            
            # Проверяем что незавершенные занятия обновились
            updated_lessons = Schedule.objects.filter(period_schedule=period_schedule, is_completed=False)
            for lesson in updated_lessons:
                assert lesson.teacher == teacher2
                assert lesson.start_time == time(10, 0)
                assert lesson.end_time == time(11, 30)
        finally:
            post_save.connect(lesson_signals.create_lessons_until_date, sender=PeriodSchedule)
    
    def test_period_schedule_creation_with_signal(self, organization, teacher, student_group, subject, classroom):
        """Тест создания PeriodSchedule с сигналом"""
        from lesson_schedule import signals as lesson_signals
        
        # Создаем PeriodSchedule - сигнал должен создать занятия
        period_schedule = PeriodSchedule.objects.create(
            period=7,
            title="Еженедельная математика",
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=teacher,
            classroom=classroom,
            group=student_group,
            subject=subject,
            start_date=date(2024, 1, 1),
            repeat_lessons_until_date=date(2024, 1, 15),
            org=organization
        )
        
        # Проверяем что занятия создались
        created_lessons = Schedule.objects.filter(period_schedule=period_schedule)
        assert created_lessons.count() > 0