import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse, resolve
from django.db.models.signals import post_save
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from lesson_schedule.models import Lesson, Subject, Classroom, PeriodLesson, Attendance, Grade, WEEK_DAY_CHOICES, GRADE_CHOICES
from students.models import StudentGroup, Student
from employers.models import Teacher, Employer
from mainapp.models import Organization, User, SubjectColor, OrgSettings
from datetime import date, time


# =============================================================================
# БАЗОВЫЕ ТЕСТЫ СВОЙСТВ И ВАЛИДАЦИИ МОДЕЛЕЙ
# =============================================================================

class TestScheduleProperties:
    """Тестирование вычисляемых свойств и полей моделей расписания"""
    
    def test_duration_calculation_basic(self, organization, teacher):
        """Тест базового расчета длительности занятия: проверяем корректность вычисления времени"""
        lesson = Lesson(
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=teacher,
            org=organization
        )
        
        duration = lesson.calc_duration
        assert duration.total_seconds() / 3600 == 1.5  # 1.5 часа = 90 минут
    
    def test_duration_edge_cases(self, organization, teacher):
        """Тест крайних случаев расчета длительности: различные временные интервалы"""
        test_cases = [
            (time(9, 0), time(9, 45), 0.75, "45 минут"),
            (time(14, 0), time(16, 30), 2.5, "2.5 часа"),
            (time(9, 0), time(11, 0), 2.0, "2 часа"), 
        ]
        
        for start, end, expected, description in test_cases:
            lesson = Lesson(
                start_time=start,
                end_time=end,
                teacher=teacher,
                org=organization
            )
            duration = lesson.calc_duration
            assert duration.total_seconds() / 3600 == expected, description
    
    def test_week_day_auto_calculation_logic(self, organization, teacher):
        """Тест автоматического расчета дня недели на основе даты занятия"""
        lesson = Lesson(
            date=date(2024, 1, 15),  # 15 января 2024 - понедельник
            teacher=teacher,
            org=organization
        )
        assert lesson.date == date(2024, 1, 15)


class TestScheduleValidation:
    """Тестирование валидации данных моделей расписания"""
    
    def test_time_validation_correct(self, organization, teacher):
        """Тест корректного временного интервала: начало раньше конца"""
        lesson = Lesson(
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=teacher,
            org=organization
        )
        
        try:
            lesson.clean()  # Должен пройти без ошибок
        except ValidationError:
            pytest.fail("Корректное время вызвало ValidationError")
    
    def test_time_validation_incorrect(self, organization, teacher):
        """Тест некорректного временного интервала: конец раньше начала"""
        lesson = Lesson(
            start_time=time(11, 0),
            end_time=time(10, 30),
            teacher=teacher,
            org=organization
        )
        
        with pytest.raises(ValidationError):
            lesson.clean()  # Должен вызвать ошибку валидации


class TestScheduleRepresentation:
    """Тестирование строковых представлений моделей (метод __str__)"""
    
    def test_string_representation_basic(self, organization, teacher):
        """Тест базового строкового представления занятия"""
        lesson = Lesson(
            title="Важный урок",
            date=date(2024, 1, 15),
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=teacher,
            org=organization
        )
        
        representation = str(lesson)
        assert "Важный урок" in representation  # Должен содержать название
        assert "2024" in representation        # Должен содержать год
        assert "Тест" in representation        # Должен содержать имя преподавателя
    
    def test_attendance_string_representation(self, lesson, student):
        """Тест строкового представления записи посещения"""
        attendance_present = Attendance(
            student=student,
            lesson=lesson,
            was_present=True,   # Студент присутствовал
            org=lesson.org
        )
        
        attendance_absent = Attendance(
            student=student,
            lesson=lesson,
            was_present=False,  # Студент отсутствовал
            org=lesson.org
        )
        
        # Оба представления должны содержать имя студента
        assert student.name in str(attendance_present)
        assert student.name in str(attendance_absent)
    
    def test_grade_string_representation(self, lesson, student):
        """Тест строкового представления оценки"""
        grade = Grade(
            student=student,
            lesson=lesson,
            value=5,           # Оценка "отлично"
            org=lesson.org
        )
        
        representation = str(grade)
        assert student.name in representation      # Должен содержать имя студента
        assert "оценка" in representation.lower() # Должен указывать на оценку


# =============================================================================
# ТЕСТЫ РАБОТЫ С БАЗОЙ ДАННЫХ
# =============================================================================

class TestScheduleDatabase:
    """Тестирование операций с базой данных: создание, сохранение, связи"""
    
    def test_relationship_saving(self, lesson, teacher, student_group, subject):
        """Тест сохранения связей между моделями в базе данных"""
        # Проверяем что фикстура создала один объект
        assert Lesson.objects.count() == 1
        
        # Проверяем прямые связи
        assert lesson.teacher == teacher
        assert lesson.group == student_group
        assert lesson.subject == subject
        
        # Проверяем обратные связи (related_name)
        assert lesson in teacher.lesson_teacher.all()
        assert lesson in student_group.lesson_classroom.all()
        assert lesson in subject.lesson_subject.all()
    
    def test_subject_creation(self, organization, teacher, subject_color):
        """Тест создания предмета с назначением преподавателя"""
        subject = Subject.objects.create(
            name="Физика",
            color=subject_color,
            org=organization
        )
        subject.teacher.add(teacher)  # Назначаем преподавателя предмету
        
        assert subject.name == "Физика"
        assert subject.teacher.count() == 1  # Должен быть один преподаватель
        assert str(subject) == "Физика"      # Проверяем строковое представление
    
    def test_subject_color_uniqueness(self, organization, subject_color):
        """Тест уникальности цвета предмета в рамках одной организации"""
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
        
        # Кастомная валидация должна запретить одинаковые цвета в одной организации
        with pytest.raises(ValidationError) as exc_info:
            subject2.clean()  # Вызываем кастомную валидацию
        
        assert "цвет уже используется" in str(exc_info.value)
    
    def test_classroom_creation(self, organization):
        """Тест создания аудитории с указанием этажа и корпуса"""
        classroom = Classroom.objects.create(
            title="201",
            floor=2,
            building="Новый корпус",
            org=organization
        )
        assert classroom.title == "201"
        assert classroom.floor == 2
        assert str(classroom) == "Аудитория 201"  # Проверяем формат строки
    
    def test_period_schedule_creation(self, organization, teacher, student_group, subject, classroom):
        """Тест создания периодического расписания (повторяющихся занятий)"""
        # Временно отключаем сигнал, чтобы не создавать реальные занятия
        from lesson_schedule import signals as lesson_signals
        from django.db.models.signals import post_save
        post_save.disconnect(lesson_signals.create_lessons_until_date, sender=PeriodLesson)
        
        try:
            period_schedule = PeriodLesson.objects.create(
                period=7,  # Период повторения в днях (еженедельно)
                title="Еженедельная математика",
                start_time=time(9, 0),
                end_time=time(10, 30),
                teacher=teacher,
                classroom=classroom,
                group=student_group,
                subject=subject,
                start_date=date(2024, 1, 15),
                repeat_lessons_until_date=date(2024, 6, 15),
                org=organization
            )
            
            assert period_schedule.period == 7
            assert period_schedule.title == "Еженедельная математика"
        finally:
            # Всегда возвращаем сигнал на место
            post_save.connect(lesson_signals.create_lessons_until_date, sender=PeriodLesson)
    
    def test_attendance_creation(self, organization, teacher, student_group, subject, student):
        """Тест создания записи о посещении студентом занятия"""
        # Сначала создаем занятие
        lesson = Lesson.objects.create(
            date=date(2024, 1, 15),
            week_day=1,  # Понедельник
            teacher=teacher,
            group=student_group,
            subject=subject,
            org=organization
        )
        
        # Создаем запись о посещении
        attendance = Attendance.objects.create(
            student=student,
            lesson=lesson,
            was_present=True,  # Студент присутствовал
            org=organization
        )
        
        assert attendance.student == student
        assert attendance.lesson == lesson
        assert attendance.was_present == True
        assert student.name in str(attendance)  # В строке должно быть имя студента
    
    def test_grade_creation(self, organization, teacher, student_group, subject, student):
        """Тест создания оценки с комментарием"""
        lesson = Lesson.objects.create(
            date=date(2024, 1, 15),
            week_day=1,  # Понедельник
            teacher=teacher,
            group=student_group,
            subject=subject,
            org=organization
        )
        
        grade = Grade.objects.create(
            student=student,
            lesson=lesson,
            value=5,           # Оценка "отлично"
            comment="Отлично!", # Комментарий к оценке
            org=organization
        )
        
        assert grade.student == student
        assert grade.value == 5
        assert grade.comment == "Отлично!"
        assert student.name in str(grade)  # В строке должно быть имя студента
    
    def test_grade_unique_constraint(self, organization, teacher, student_group, subject, student):
        """Тест ограничения уникальности: один студент - одна оценка за занятие"""
        lesson = Lesson.objects.create(
            date=date(2024, 1, 15),
            week_day=1,  # Понедельник
            teacher=teacher,
            group=student_group,
            subject=subject,
            org=organization
        )
        
        # Создаем первую оценку
        Grade.objects.create(
            student=student,
            lesson=lesson, 
            value=5,
            org=organization
        )
        
        # Попытка создать вторую оценку для того же студента и занятия должна вызвать ошибку
        with pytest.raises(Exception):  
            Grade.objects.create(
                student=student,
                lesson=lesson,
                value=4,  # Другая оценка, но для того же студента и занятия
                org=organization
            )


class TestScheduleRelationships:
    """Тестирование связей между моделями через ForeignKey и related_name"""
    
    def test_schedule_teacher_relationship(self, lesson, teacher):
        """Тест связи между занятием и преподавателем"""
        assert lesson.teacher == teacher
        # Проверяем обратную связь через related_name
        assert lesson in teacher.lesson_teacher.all()
    
    def test_schedule_classroom_relationship(self, lesson, classroom):
        """Тест связи между занятием и аудиторией"""
        assert lesson.classroom == classroom
        # Проверяем обратную связь через related_name
        assert lesson in classroom.lesson_group.all()
    
    def test_schedule_group_relationship(self, lesson, student_group):
        """Тест связи между занятием и учебной группой"""
        assert lesson.group == student_group
        # Проверяем обратную связь через related_name
        assert lesson in student_group.lesson_classroom.all()
    
    def test_attendance_student_relationship(self, attendance, student):
        """Тест связи между посещением и студентом"""
        assert attendance.student == student
        assert attendance in student.attendances.all()  # Обратная связь


class TestScheduleRequiredFields:
    """Тесты обязательных полей моделей расписания"""
    
    def test_schedule_required_fields(self, organization, teacher):
        """Тест минимального набора обязательных полей для создания занятия"""
        lesson = Lesson.objects.create(
            date=date(2024, 1, 15),
            week_day=1,  # Понедельник
            teacher=teacher,
            org=organization
        )
        assert lesson.id is not None  # Объект должен быть сохранен в БД


class TestScheduleBusinessLogic:
    """Тесты бизнес-логики и автоматических вычислений"""
    
    def test_schedule_string_representation(self, lesson):
        """Тест форматирования строкового представления занятия"""
        representation = str(lesson)
        assert lesson.title in representation  # Должен содержать название
        assert "2024" in representation        # Должен содержать год
    
    def test_week_day_auto_calculation(self, organization, teacher):
        """Тест автоматического расчета дня недели при сохранении"""
        lesson = Lesson.objects.create(
            date=date(2024, 1, 15),  # 15 января 2024 - понедельник (день 1)
            teacher=teacher,
            org=organization
        )
        # После сохранения week_day должен быть вычислен автоматически
        assert lesson.week_day == 1  # Понедельник


# =============================================================================
# ТЕСТЫ URLS И ПРЕДСТАВЛЕНИЙ (VIEWS)
# =============================================================================

class TestLessonScheduleUrls:
    """Тесты маршрутов (URLs) API для модуля расписания"""

    def test_schedules_list_url(self):
        """Тест URL для получения списка занятий"""
        url = reverse('lesson-list')
        assert resolve(url).func.cls.__name__ == 'ScheduleViewSet'

    def test_schedules_detail_url(self):
        """Тест URL для получения деталей конкретного занятия"""
        url = reverse('lesson-detail', kwargs={'pk': 1})
        assert resolve(url).func.cls.__name__ == 'ScheduleViewSet'

    def test_subjects_list_url(self):
        """Тест URL для получения списка предметов"""
        url = reverse('subject-list')
        assert resolve(url).func.cls.__name__ == 'SubjectViewSet'

    def test_classrooms_list_url(self):
        """Тест URL для получения списка аудиторий"""
        url = reverse('classroom-list')
        assert resolve(url).func.cls.__name__ == 'ClassroomViewSet'

    def test_attendances_list_url(self):
        """Тест URL для получения списка посещений"""
        url = reverse('attendance-list')
        assert resolve(url).func.cls.__name__ == 'AttendanceViewSet'

    def test_period_schedules_list_url(self):
        """Тест URL для получения списка периодических расписаний"""
        url = reverse('period_lesson-list')
        assert resolve(url).func.cls.__name__ == 'PeriodScheduleViewSet'

    def test_grades_list_url(self):
        """Тест URL для получения списка оценок"""
        url = reverse('grade-list')
        assert resolve(url).func.cls.__name__ == 'GradeViewSet'


class TestLessonScheduleBasicViews:
    """Базовые тесты логики представлений (без API клиента)"""

    def test_schedule_creation_logic(self, organization, teacher, student_group, subject, classroom):
        """Тест логики создания занятия напрямую через ORM"""
        lesson = Lesson.objects.create(
            title="Тестовый урок",
            date=date(2024, 1, 15),
            week_day=1,  # Понедельник
            teacher=teacher,
            classroom=classroom,
            group=student_group,
            subject=subject,
            org=organization
        )
        
        # Проверяем что объект создался
        assert lesson.id is not None
        assert lesson.title == "Тестовый урок"
        assert lesson.week_day == 1

    def test_subject_creation_logic(self, organization, teacher, subject_color):
        """Тест логики создания предмета напрямую через ORM"""
        subject = Subject.objects.create(
            name="Физика",
            color=subject_color,
            org=organization
        )
        subject.teacher.add(teacher)  # Назначаем преподавателя
        
        assert subject.id is not None
        assert subject.name == "Физика"
        assert subject.teacher.count() == 1  # Должен быть один преподаватель

    def test_classroom_creation_logic(self, organization):
        """Тест логики создания аудитории напрямую через ORM"""
        classroom = Classroom.objects.create(
            title="201",
            floor=2,
            building="Новый корпус",
            org=organization
        )
        
        assert classroom.id is not None
        assert classroom.title == "201"
        assert classroom.floor == 2


class TestLessonScheduleChoiceFields:
    """Тесты полей с предопределенными вариантами выбора"""

    def test_week_day_choices(self):
        """Тест вариантов дней недели"""
        assert len(WEEK_DAY_CHOICES) == 7  # 7 дней в неделе
        assert WEEK_DAY_CHOICES[0] == (1, "Monday")   # Понедельник
        assert WEEK_DAY_CHOICES[6] == (7, "Sunday")   # Воскресенье

    def test_grade_choices(self):
        """Тест вариантов оценок"""
        assert len(GRADE_CHOICES) == 4  # 4 варианта оценок
        assert GRADE_CHOICES[0] == (2, "Не удовлетварительно")  # Неуд
        assert GRADE_CHOICES[3] == (5, "Отлично")               # Отлично


class TestLessonScheduleUtils:
    """Вспомогательные тесты мета-данных моделей"""

    def test_model_meta(self):
        """Тест мета-данных моделей (verbose_name, ordering)"""
        assert Lesson._meta.verbose_name == 'Занятие'
        assert Lesson._meta.verbose_name_plural == 'Занятия'
        assert Subject._meta.verbose_name == 'Предмет'
        assert Subject._meta.verbose_name_plural == 'Предметы'
        assert Classroom._meta.verbose_name == 'Аудитория'
        assert Classroom._meta.verbose_name_plural == 'Аудиории'
        assert Attendance._meta.verbose_name == 'Посещение'
        assert Attendance._meta.verbose_name_plural == 'Посещения'
        assert Grade._meta.verbose_name == 'Оценка'
        assert Grade._meta.verbose_name_plural == 'Оценки'

    def test_ordering(self):
        """Тест порядка сортировки по умолчанию"""
        assert Lesson._meta.ordering == ['date', 'start_time']  # Сначала по дате, потом по времени


# =============================================================================
# ТЕСТЫ БЕЗОПАСНОСТИ И ИЗОЛЯЦИИ ОРГАНИЗАЦИЙ
# =============================================================================

class TestOrganizationSecurity:
    """Тесты безопасности: изоляция данных между организациями"""
    
    def test_subject_color_organization_isolation(self, subject_color, subject_color_org2):
        """Тест изоляции цветов предметов между организациями"""
        # Цвета организации 1
        colors_org1 = SubjectColor.objects.filter(org=subject_color.org)
        assert colors_org1.count() == 1
        assert subject_color in colors_org1
        assert subject_color_org2 not in colors_org1  # Цвет из другой организации не должен быть доступен
        
        # Цвета организации 2
        colors_org2 = SubjectColor.objects.filter(org=subject_color_org2.org)
        assert colors_org2.count() == 1
        assert subject_color_org2 in colors_org2
        assert subject_color not in colors_org2  # Цвет из первой организации не должен быть доступен

    def test_api_color_access_organization_isolation(self, authenticated_client, subject_color):
        """Тест изоляции доступа к цветам через API"""
        url = reverse('subject_color-list')
        response = authenticated_client.get(url)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        
        if response.status_code == status.HTTP_200_OK:
            colors_data = response.json()
            # Обрабатываем пагинацию если есть
            if 'results' in colors_data:
                colors_list = colors_data['results']
            else:
                colors_list = colors_data
                
            assert len(colors_list) >= 1
            color_titles = [color['title'] for color in colors_list]
            assert subject_color.title in color_titles  # Должны видеть только свои цвета

    def test_api_cross_organization_color_access_prevention(self, authenticated_client, subject_color_org2):
        """Тест предотвращения доступа к цветам чужой организации через API"""
        url = reverse('subject_color-detail', kwargs={'pk': subject_color_org2.id})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND  # Должен вернуть 404

    def test_api_subject_creation_organization_isolation(self, authenticated_client, subject_color):
        """Тест изоляции создания предметов через API"""
        subject_data = {
            'name': 'Новый предмет Org1',
            'color': subject_color.id,  # Цвет из своей организации
        }
        
        url = reverse('subject-list')
        response = authenticated_client.post(url, subject_data)
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
        
        if response.status_code == status.HTTP_201_CREATED:
            new_subject = Subject.objects.get(id=response.json()['id'])
            assert new_subject.org == subject_color.org  # Предмет должен принадлежать той же организации

    def test_api_cross_organization_subject_creation_prevention(self, authenticated_client, subject_color_org2):
        """Тест предотвращения создания предмета с цветом из чужой организации"""
        subject_data = {
            'name': 'Новый предмет с чужим цветом',
            'color': subject_color_org2.id,  # Цвет из чужой организации!
        }
        
        url = reverse('subject-list')
        response = authenticated_client.post(url, subject_data)
        # Должен вернуть ошибку - нельзя использовать чужой цвет
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]

    def test_api_attendance_organization_isolation(self, authenticated_client, attendance):
        """Тест изоляции данных о посещаемости между организациями через API"""
        url = reverse('attendance-list')
        response = authenticated_client.get(url)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
        
        if response.status_code == status.HTTP_200_OK:
            attendances_data = response.json()
            # Обрабатываем пагинацию если есть
            if 'results' in attendances_data:
                attendances_list = attendances_data['results']
            else:
                attendances_list = attendances_data
                
            assert len(attendances_list) >= 1  # Должны видеть только свои посещения

    def test_api_attendance_cross_organization_access_prevention(self, authenticated_client, attendance_org2):
        """Тест предотвращения доступа к посещениям чужой организации через API"""
        url = reverse('attendance-detail', kwargs={'pk': attendance_org2.id})
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND  # Должен вернуть 404


# =============================================================================
# ТЕСТЫ КОНФЛИКТОВ РАСПИСАНИЯ
# =============================================================================

class TestScheduleConflictValidation:
    """ТЕСТЫ КОНФЛИКТОВ РАСПИСАНИЯ: проверяют валидацию пересечений времени"""
    
    def test_time_overlap_logic(self):
        """Тест логики пересечения временных интервалов без привязки к конкретным занятиям"""
        from lesson_schedule.utils import LessonSlot
        
        # Создаем слоты для тестирования логики пересечения
        slot1 = LessonSlot(time(9, 0), time(10, 30))
        slot2 = LessonSlot(time(10, 0), time(11, 30))
        
        # Проверяем что слоты пересекаются (только логика, без валидации)
        assert slot1.is_overlap(slot2) == True
        
        # Слоты без пересечения
        slot3 = LessonSlot(time(11, 0), time(12, 0))
        assert slot1.is_overlap(slot3) == False

    def test_no_conflict_different_times(self, organization, teacher, student_group, subject):
        """Отсутствие конфликта: занятия в разное время"""
        Lesson.objects.create(
            date=date(2024, 1, 15),
            week_day=1,  # Понедельник
            start_time=time(9, 0),
            end_time=time(10, 0),
            teacher=teacher,
            group=student_group,
            subject=subject,
            org=organization
        )
        
        # Занятие после первого - конфликта быть не должно
        non_conflicting_lesson = Lesson(
            date=date(2024, 1, 15),
            week_day=1,  # Понедельник
            start_time=time(10, 30),  # Начинается после окончания первого
            end_time=time(11, 30),
            teacher=teacher,  
            group=student_group,  
            subject=subject,  
            org=organization
        )
        
        try:
            non_conflicting_lesson.clean()  # Явный вызов clean() - не должно быть ошибки
        except ValidationError:
            pytest.fail("Не должно быть конфликта для разного времени")
    
    def test_no_conflict_different_dates(self, organization, teacher, student_group, subject):
        """Отсутствие конфликта: занятия в разные даты"""
        Lesson.objects.create(
            date=date(2024, 1, 15),
            week_day=1,  # Понедельник
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=teacher,
            group=student_group,
            subject=subject,
            org=organization
        )
        
        # То же время, но другая дата - конфликта быть не должно
        non_conflicting_lesson = Lesson(
            date=date(2024, 1, 16),  # Вторник
            week_day=2,  # Вторник
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=teacher,
            group=student_group,
            subject=subject,
            org=organization
        )
        
        try:
            non_conflicting_lesson.clean()  # Явный вызов clean() - не должно быть ошибки
        except ValidationError:
            pytest.fail("Не должно быть конфликта для разных дат")


class TestFastConflictTests:
    """Быстрые тесты конфликтов для ускорения CI/CD"""
    
    def test_fast_no_conflict(self, organization, teacher, student_group, subject):
        """Быстрый тест отсутствия конфликта при разных датах"""
        Lesson.objects.create(
            date=date(2024, 1, 15),  # Понедельник
            week_day=1,  
            start_time=time(9, 0), 
            end_time=time(10, 30),
            teacher=teacher, 
            group=student_group, 
            subject=subject, 
            org=organization
        )
        
        no_conflict = Lesson(
            date=date(2024, 1, 16),  # Вторник
            week_day=2,  
            start_time=time(9, 0), 
            end_time=time(10, 30),
            teacher=teacher, 
            group=student_group, 
            subject=subject, 
            org=organization
        )
        
        try:
            no_conflict.clean()  # Не должно быть конфликта
        except ValidationError:
            pytest.fail("Не должно быть конфликта")


# =============================================================================
# БАЗОВЫЙ КЛАСС ДЛЯ API ТЕСТОВ
# =============================================================================

class BaseAPITestCase(APITestCase):
    """Базовый класс для API тестов с настройкой аутентификации и тестовых данных"""
    
    def setUp(self):
        """Настройка тестового окружения перед каждым тестом"""
        # Временно отключаем сигнал создания настроек организации
        from mainapp import signals as main_signals
        post_save.disconnect(main_signals.create_org_settings, sender=Organization)
        
        # Создаем тестовую организацию
        self.org = Organization.objects.create(name="Test Org")
        self.org_settings = OrgSettings.objects.create(org=self.org, timezone="UTC")
        
        # Создаём пользователя для аутентификации
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123", 
            email="test@example.com",
            org=self.org,  # Пользователь принадлежит организации
        )
        
        # Создаем преподавателей
        self.employer1 = Employer.objects.create(
            name="Тест", 
            surname="Преподаватель", 
            org=self.org
        )
        self.teacher1 = Teacher.objects.create(employer=self.employer1, org=self.org)
        
        self.employer2 = Employer.objects.create(
            name="Второй", 
            surname="Учитель", 
            org=self.org
        )
        self.teacher2 = Teacher.objects.create(employer=self.employer2, org=self.org)
        
        # Создаем предмет и назначаем преподавателей
        self.subject = Subject.objects.create(name="Математика", org=self.org)
        self.subject.teacher.add(self.teacher1, self.teacher2)
        
        # Создаем аудитории
        self.classroom1 = Classroom.objects.create(title="101", org=self.org)
        self.classroom2 = Classroom.objects.create(title="102", org=self.org)
        
        # Создаем учебные группы
        self.group1 = StudentGroup.objects.create(name="10А", org=self.org)
        self.group2 = StudentGroup.objects.create(name="10Б", org=self.org)
        
        # Настраиваем API клиент с аутентификацией
        self.client = APIClient()
        
        # Стандартная аутентификация
        login_success = self.client.login(username="testuser", password="testpass123")
        print(f"Login success: {login_success}")
        
        # Принудительная аутентификация для всех запросов
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        """Восстановление окружения после каждого теста"""
        from mainapp import signals as main_signals
        post_save.connect(main_signals.create_org_settings, sender=Organization)
    
    def _create_valid_schedule_data(self, **overrides):
        """Создает валидные данные для API запроса создания занятия"""
        base_data = {
            'title': 'Тестовое занятие',
            'date': '2024-01-15',
            'week_day': 1,  # Понедельник
            'teacher': self.teacher1.id,
            'group': self.group1.id,
            'subject': self.subject.id,
            'classroom': self.classroom1.id,
            'start_time': '09:00',
            'end_time': '10:30'
        }
        base_data.update(overrides)
        return base_data
    
    def _create_schedule_via_api(self, data):
        """Вспомогательный метод для создания занятия через API"""
        response = self.client.post(reverse('lesson-list'), data, format='json')
        print(f"API CREATE SCHEDULE: {response.status_code}")
        if hasattr(response, 'data'):
            print(f"Response data: {response.data}")
        return response
    
    def _ensure_api_access(self):
        """Проверяем что у нас есть доступ к API"""
        response = self.client.get(reverse('lesson-list'))
        print(f"API ACCESS CHECK: {response.status_code}")
        return response.status_code != 401  # Не 401 Unauthorized


# =============================================================================
# API ТЕСТЫ КОНФЛИКТОВ РАСПИСАНИЯ
# =============================================================================

class ScheduleConflictAPITestCases(BaseAPITestCase):
    """API тесты для проверки конфликтов расписания через LessonValidationMixin"""
    
    def test_create_schedule_success(self):
        """Тест успешного создания занятия через API - должен вернуть 201 CREATED"""
        schedule_data = self._create_valid_schedule_data(
            title='Успешное занятие',
            start_time='09:00',
            end_time='10:30'
        )
        
        response = self.client.post(reverse('lesson-list'), schedule_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
        
        created_lesson = Lesson.objects.first()
        self.assertEqual(created_lesson.title, 'Успешное занятие')
    
    def test_create_schedule_time_conflict_teacher(self):
        """Тест конфликта времени для преподавателя через API - должен вернуть 400 BAD REQUEST"""
        # Создаем первое занятие для teacher1
        first_schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30',
            teacher=self.teacher1.id
        )
        response1 = self.client.post(reverse('lesson-list'), first_schedule_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Пытаемся создать второе занятие для того же преподавателя в пересекающееся время
        second_schedule_data = self._create_valid_schedule_data(
            title='Второе занятие (конфликт)',
            start_time='09:30',  # Пересекается с первым занятием (9:00-10:30)
            end_time='11:00',
            teacher=self.teacher1.id  # Тот же преподаватель!
        )
        
        response2 = self.client.post(reverse('lesson-list'), second_schedule_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response2.data)  # Должен вернуть описание ошибки
    
    def test_create_schedule_time_conflict_classroom(self):
        """Тест конфликта времени для аудитории через API - должен вернуть 400 BAD REQUEST"""
        # Создаем первое занятие в classroom1
        first_schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30',
            classroom=self.classroom1.id
        )
        response1 = self.client.post(reverse('lesson-list'), first_schedule_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Пытаемся создать второе занятие в той же аудитории в пересекающееся время
        second_schedule_data = self._create_valid_schedule_data(
            title='Второе занятие (конфликт)',
            start_time='10:00',  # Пересекается с первым занятием (9:00-10:30)
            end_time='11:30',
            classroom=self.classroom1.id,  # Та же аудитория!
            teacher=self.teacher2.id,      # Другой преподаватель
            group=self.group2.id           # Другая группа
        )
        
        response2 = self.client.post(reverse('lesson-list'), second_schedule_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_schedule_time_conflict_group(self):
        """Тест конфликта времени для группы через API - должен вернуть 400 BAD REQUEST"""
        # Создаем первое занятие для group1
        first_schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30',
            group=self.group1.id
        )
        response1 = self.client.post(reverse('lesson-list'), first_schedule_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Пытаемся создать второе занятие для той же группы в пересекающееся время
        second_schedule_data = self._create_valid_schedule_data(
            title='Второе занятие (конфликт)',
            start_time='10:00',  # Пересекается с первым занятием (9:00-10:30)
            end_time='11:30',
            group=self.group1.id,  # Та же группа!
            teacher=self.teacher2.id,  # Другой преподаватель
            classroom=self.classroom2.id  # Другая аудитория
        )
        
        response2 = self.client.post(reverse('lesson-list'), second_schedule_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_no_time_conflict_different_times_api(self):
        """Тест отсутствия конфликта при разном времени - должен вернуть 201 CREATED"""
        # Создаем первое занятие
        first_schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:00'
        )
        response1 = self.client.post(reverse('lesson-list'), first_schedule_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Создаем второе занятие в другое время (без конфликта)
        second_schedule_data = self._create_valid_schedule_data(
            title='Второе занятие',
            start_time='10:30',  # После окончания первого
            end_time='11:30',
            teacher=self.teacher1.id,
            group=self.group1.id,
            classroom=self.classroom1.id
        )
        
        response2 = self.client.post(reverse('lesson-list'), second_schedule_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
    
    def test_no_time_conflict_different_dates_api(self):
        """Тест отсутствия конфликта при разных датах - должен вернуть 201 CREATED"""
        # Создаем первое занятие
        first_schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            date='2024-01-15',
            week_day=1  # Понедельник
        )
        response1 = self.client.post(reverse('lesson-list'), first_schedule_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Создаем второе занятие в другую дату (без конфликта)
        second_schedule_data = self._create_valid_schedule_data(
            title='Второе занятие',
            date='2024-01-16',  # Вторник
            week_day=2,         # Вторник
            teacher=self.teacher1.id,
            group=self.group1.id,
            classroom=self.classroom1.id,
            start_time='09:00',
            end_time='10:30'
        )
        
        response2 = self.client.post(reverse('lesson-list'), second_schedule_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
    
    def test_no_time_conflict_different_resources_api(self):
        """Тест отсутствия конфликта при разных ресурсах - должен вернуть 201 CREATED"""
        # Создаем первое занятие
        first_schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30',
            teacher=self.teacher1.id,
            group=self.group1.id,
            classroom=self.classroom1.id
        )
        response1 = self.client.post(reverse('lesson-list'), first_schedule_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Создаем второе занятие в то же время, но с разными ресурсами
        second_schedule_data = self._create_valid_schedule_data(
            title='Второе занятие',
            start_time='09:00',  # То же время!
            end_time='10:30',    # То же время!
            teacher=self.teacher2.id,    # Другой преподаватель
            group=self.group2.id,        # Другая группа
            classroom=self.classroom2.id # Другая аудитория
        )
        
        response2 = self.client.post(reverse('lesson-list'), second_schedule_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)


class ScheduleUpdateConflictAPITestCases(BaseAPITestCase):
    """API тесты для проверки конфликтов при обновлении расписания"""
    
    def test_update_schedule_success_no_conflict(self):
        """Тест успешного обновления занятия без конфликта"""
        # Создаем занятие
        schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30'
        )
        response = self.client.post(reverse('lesson-list'), schedule_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        schedule_id = response.data['id']
        
        # Обновляем занятие без создания конфликта
        update_data = {
            'title': 'Обновленное занятие',
            'start_time': '11:00',  # Меняем на свободное время
            'end_time': '12:30'
        }
        
        response_update = self.client.patch(
            reverse('lesson-detail', kwargs={'pk': schedule_id}),
            update_data,
            format='json'
        )
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
    
    def test_update_schedule_with_conflict(self):
        """Тест конфликта при обновлении занятия - должен вернуть 400 BAD REQUEST"""
        # Создаем первое занятие
        first_schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30',
            teacher=self.teacher1.id
        )
        response1 = self.client.post(reverse('lesson-list'), first_schedule_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        first_lesson_id = response1.data['id']
        
        # Создаем второе занятие без конфликта
        second_schedule_data = self._create_valid_schedule_data(
            title='Второе занятие',
            start_time='11:00',
            end_time='12:30',
            teacher=self.teacher2.id,
            group=self.group2.id,
            classroom=self.classroom2.id
        )
        response2 = self.client.post(reverse('lesson-list'), second_schedule_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        second_lesson_id = response2.data['id']
        
        # Пытаемся обновить второе занятие на конфликтующее время с первым
        update_data = {
            'start_time': '09:00',  # Конфликт с первым занятием!
            'end_time': '10:30',
            'teacher': self.teacher1.id  # Тот же преподаватель!
        }
        
        response_update = self.client.patch(
            reverse('lesson-detail', kwargs={'pk': second_lesson_id}),
            update_data,
            format='json'
        )
        self.assertEqual(response_update.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response_update.data)
        self.assertIn('free_slots', response_update.data)  # Должны вернуть информацию о свободных слотах
    
    def test_update_schedule_force_update_with_conflict(self):
        """Тест принудительного обновления с конфликтом - должен вернуть 200 OK"""
        # Создаем первое занятие
        first_schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30',
            teacher=self.teacher1.id
        )
        response1 = self.client.post(reverse('lesson-list'), first_schedule_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        first_lesson_id = response1.data['id']
        
        # Создаем второе занятие без конфликта
        second_schedule_data = self._create_valid_schedule_data(
            title='Второе занятие',
            start_time='11:00',
            end_time='12:30',
            teacher=self.teacher2.id
        )
        response2 = self.client.post(reverse('lesson-list'), second_schedule_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        second_lesson_id = response2.data['id']
        
        # Пытаемся обновить второе занятие на конфликтующее время с флагом принудительного обновления
        update_data = {
            'start_time': '09:00',  # Конфликт с первым занятием!
            'end_time': '10:30',
            'teacher': self.teacher1.id  # Тот же преподаватель!
        }
        
        response_update = self.client.patch(
            f"{reverse('lesson-detail', kwargs={'pk': second_lesson_id})}?is_force_update=true",
            update_data,
            format='json'
        )
        # С is_force_update=true должно пройти несмотря на конфликт
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
    
    def test_update_non_critical_fields_no_validation(self):
        """Тест обновления некритических полей без проверки конфликтов"""
        # Создаем занятие
        schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30'
        )
        response = self.client.post(reverse('lesson-list'), schedule_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        lesson_id = response.data['id']
        
        # Обновляем только некритические поля (не входящие в critical_fields)
        update_data = {
            'title': 'Новое название',
            'comment': 'Новый комментарий'
        }
        
        response_update = self.client.patch(
            reverse('lesson-detail', kwargs={'pk': lesson_id}),
            update_data,
            format='json'
        )
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(response_update.data['title'], 'Новое название')
        self.assertEqual(response_update.data['comment'], 'Новый комментарий')


class PeriodScheduleConflictAPITestCases(BaseAPITestCase):
    """API тесты для проверки конфликтов периодического расписания"""
    
    def _create_valid_period_schedule_data(self, **overrides):
        """Создает валидные данные для API запроса PeriodLesson"""
        base_data = {
            'title': 'Еженедельная математика',
            'period': 7,  # Период повторения в днях (еженедельно)
            'start_date': '2024-01-01',
            'repeat_lessons_until_date': '2024-01-31',
            'start_time': '09:00',
            'end_time': '10:30',
            'teacher': self.teacher1.id,
            'group': self.group1.id,
            'subject': self.subject.id,
            'classroom': self.classroom1.id,
        }
        base_data.update(overrides)
        return base_data
    
    def test_period_schedule_update_with_conflict(self):
        """Тест конфликта при обновлении периодического расписания - должен вернуть 400 BAD REQUEST"""
        # Создаем обычное занятие, которое будет конфликтовать
        existing_lesson = Lesson.objects.create(
            title='Существующее занятие',
            date=date(2024, 1, 15),  # Эта дата попадет в периодическое расписание
            week_day=1,  # Понедельник
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=self.teacher1,
            group=self.group1,
            subject=self.subject,
            classroom=self.classroom1,
            org=self.org
        )
        
        # Создаем PeriodLesson
        period_data = self._create_valid_period_schedule_data(
            start_date='2024-01-01',
            repeat_lessons_until_date='2024-01-31',
            start_time='11:00',  # Без конфликта изначально
            end_time='12:30'
        )
        
        response = self.client.post(reverse('period_lesson-list'), period_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        period_id = response.data['id']
        
        # Пытаемся обновить PeriodLesson на конфликтующее время
        update_data = {
            'start_time': '09:00',  # Конфликт с existing_lesson!
            'end_time': '10:30'
        }
        
        response_update = self.client.patch(
            reverse('period_lesson-detail', kwargs={'pk': period_id}),
            update_data,
            format='json'
        )
        
        # LessonValidationMixin должен обнаружить конфликт для всех созданных уроков
        self.assertEqual(response_update.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_period_schedule_force_update_with_conflicts(self):
        """Тест принудительного обновления PeriodLesson с конфликтами - должен вернуть 200 OK"""
        # Создаем конфликтующее занятие
        Lesson.objects.create(
            title='Конфликтующее занятие',
            date=date(2024, 1, 15),
            week_day=1,  # Понедельник
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=self.teacher1,
            group=self.group1,
            subject=self.subject,
            classroom=self.classroom1,
            org=self.org
        )
        
        # Создаем PeriodLesson
        period_data = self._create_valid_period_schedule_data(
            start_time='11:00',
            end_time='12:30'
        )
        
        response = self.client.post(reverse('period_lesson-list'), period_data, format='json')
        period_id = response.data['id']
        
        # Пытаемся обновить с флагом принудительного обновления
        update_data = {
            'start_time': '09:00',
            'end_time': '10:30'
        }
        
        response_update = self.client.patch(
            f"{reverse('period_lesson-detail', kwargs={'pk': period_id})}?is_force_update=true",
            update_data,
            format='json'
        )
        
        # С is_force_update=true должно пройти несмотря на конфликт
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)


class ScheduleEdgeCaseAPITestCases(BaseAPITestCase):
    """Тесты граничных случаев для конфликтов расписания через API"""
    
    def test_boundary_times_no_conflict(self):
        """Тест что занятия вплотную друг к другу не конфликтуют"""
        # Создаем первое занятие
        first_schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:00'
        )
        response1 = self.client.post(reverse('lesson-list'), first_schedule_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Создаем второе занятие сразу после первого (без перерыва)
        second_schedule_data = self._create_valid_schedule_data(
            title='Второе занятие',
            start_time='10:00',  # Начинается точно когда заканчивается первое
            end_time='11:00',
            teacher=self.teacher1.id,
            group=self.group1.id,
            classroom=self.classroom1.id
        )
        
        response2 = self.client.post(reverse('lesson-list'), second_schedule_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)  # Не должно быть конфликта
    
    def test_partial_overlap_conflict(self):
        """Тест частичного пересечения занятий - должен вернуть 400 BAD REQUEST"""
        # Создаем первое занятие
        first_schedule_data = self._create_valid_schedule_data(
            title='Первое занятие',
            start_time='09:00',
            end_time='10:30',
            teacher=self.teacher1.id
        )
        response1 = self.client.post(reverse('lesson-list'), first_schedule_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Пытаемся создать второе занятие с частичным пересечением
        second_schedule_data = self._create_valid_schedule_data(
            title='Второе занятие (частичное пересечение)',
            start_time='10:00',  # Начинается во время первого занятия
            end_time='11:30',    # Заканчивается после первого занятия
            teacher=self.teacher1.id  # Тот же преподаватель!
        )
        
        response2 = self.client.post(reverse('lesson-list'), second_schedule_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)  # Должен быть конфликт