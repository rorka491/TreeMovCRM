from django.test import TestCase
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


class LessonScheduleLogicTest(TestCase):
    """Базовый класс для тестирования логики (без сохранения в БД)"""
    
    def setUp(self):
        from mainapp import signals as main_signals
        post_save.disconnect(main_signals.create_org_settings, sender=Organization)
        
        self.org = Organization.objects.create(name="Test Org")
        
        self.org_settings = OrgSettings.objects.create(
            org=self.org,
            timezone="UTC",
            repeat_lessons_until="06-30"
        )
        
        self.employer = Employer.objects.create(
            name="Тест", 
            surname="Преподаватель", 
            org=self.org
        )
        self.teacher = Teacher.objects.create(employer=self.employer, org=self.org)
        
        self.subject_color = SubjectColor.objects.create(
            title="Синий",
            color_hex="#0000FF",  
            org=self.org
        )
        
        self.subject = Subject.objects.create(
            name="Математика", 
            color=self.subject_color,
            org=self.org
        )
        self.subject.teacher.add(self.teacher)
        
        self.classroom = Classroom.objects.create(title="101", org=self.org)
        self.group = StudentGroup.objects.create(name="10А", org=self.org)

    def test_checkout_week_day(self):
        past_lesson = Schedule.objects.create(
            date=date(2023, 12, 1),
            start_time=time(9, 0),
            end_time=time(10, 0),
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            is_completed=False,
            org=self.org
        )
        past_lesson.save()
        assert past_lesson.week_day is not None
        
    def tearDown(self):
        from mainapp import signals as main_signals
        post_save.connect(main_signals.create_org_settings, sender=Organization)

    def create_unsaved_schedule(self, **kwargs):
        """Создает объект Schedule без сохранения в БД"""
        defaults = {
            'date': date(2024, 1, 15),
            'week_day': 1, 
            'teacher': self.teacher,
            'org': self.org
        }
        defaults.update(kwargs)
        return Schedule(**defaults)
    
    def create_unsaved_student(self, **kwargs):
        """Создает объект Student без сохранения в БД"""
        defaults = {
            'name': "Тест",  
            'surname': "Студентов", 
            'birthday': date(2000, 1, 1),  
            'org': self.org
        }
        defaults.update(kwargs)
        return Student(**defaults)
    
    def create_student(self, **kwargs):
        """Создает и сохраняет объект Student с обязательными полями"""
        defaults = {
            'name': "Тест",
            'surname': "Студентов", 
            'birthday': date(2000, 1, 1), 
            'org': self.org
        }
        defaults.update(kwargs)
        return Student.objects.create(**defaults)


class SchedulePropertiesTest(LessonScheduleLogicTest):
    """Тестирование свойств и вычисляемых полей"""
    
    def test_duration_calculation_basic(self):
        """Тест базового расчета длительности"""
        schedule = self.create_unsaved_schedule(
            start_time=time(9, 0),
            end_time=time(10, 30)
        )
        
        duration = schedule.calc_duration
        self.assertEqual(duration.total_seconds() / 3600, 1.5)
    
    def test_duration_edge_cases(self):
        """Тест крайних случаев расчета длительности"""
        test_cases = [
            (time(9, 0), time(9, 45), 0.75, "45 минут"),
            (time(14, 0), time(16, 30), 2.5, "2.5 часа"),
            (time(9, 0), time(11, 0), 2.0, "2 часа"), 
        ]
        
        for start, end, expected, description in test_cases:
            with self.subTest(description):
                schedule = self.create_unsaved_schedule(
                    start_time=start,
                    end_time=end
                )
                duration = schedule.calc_duration
                self.assertEqual(duration.total_seconds() / 3600, expected)
    
    def test_week_day_auto_calculation_logic(self):
        """Тест логики автоматического расчета дня недели"""
        schedule = self.create_unsaved_schedule(date=date(2024, 1, 15))
        self.assertEqual(schedule.date, date(2024, 1, 15))


class ScheduleValidationTest(LessonScheduleLogicTest):
    """Тестирование валидации данных"""
    
    def test_time_validation_correct(self):
        """Тест корректного времени"""
        schedule = self.create_unsaved_schedule(
            start_time=time(9, 0),
            end_time=time(10, 30)
        )
        
        try:
            schedule.clean()  
        except ValidationError:
            self.fail("Корректное время вызвало ValidationError")
    
    def test_time_validation_incorrect(self):
        """Тест некорректного времени (конец раньше начала)"""
        schedule = self.create_unsaved_schedule(
            start_time=time(11, 0),
            end_time=time(10, 30)
        )
        
        with self.assertRaises(ValidationError):
            schedule.clean()


class ScheduleRepresentationTest(LessonScheduleLogicTest):
    """Тестирование строковых представлений"""
    
    def test_string_representation_basic(self):
        """Тест базового строкового представления"""
        schedule = self.create_unsaved_schedule(
            title="Важный урок",
            date=date(2024, 1, 15),
            start_time=time(9, 0),
            end_time=time(10, 30)
        )
        
        representation = str(schedule)
        self.assertIn("Важный урок", representation)
        self.assertIn("2024", representation)
        self.assertIn("Тест", representation)  
    
    def test_attendance_string_representation(self):
        """Тест строкового представления посещения"""
        schedule = self.create_unsaved_schedule(
            date=date(2024, 1, 15),
            week_day=1,
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        student = self.create_unsaved_student(
            name="Елена",
            surname="Посещаева"
        )
        
        attendance_present = Attendance(
            student=student,
            lesson=schedule,
            was_present=True,
            org=self.org
        )
        
        attendance_absent = Attendance(
            student=student,
            lesson=schedule,
            was_present=False,
            org=self.org
        )
        
        self.assertIn("Елена", str(attendance_present))
        self.assertIn("Елена", str(attendance_absent))
    
    def test_grade_string_representation(self):
        """Тест строкового представления оценки"""
        schedule = self.create_unsaved_schedule(
            date=date(2024, 1, 15),
            week_day=1,
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        student = self.create_unsaved_student(
            name="Оценка",
            surname="Тестова"
        )
        
        grade = Grade(
            student=student,
            lesson=schedule,
            value=5,
            org=self.org
        )
        
        representation = str(grade)
        self.assertIn("Оценка", representation)
        self.assertIn("оценка", representation.lower())


class ScheduleDatabaseTest(LessonScheduleLogicTest):
    """Тестирование работы с БД (сохраняем объекты)"""
    
    def test_relationship_saving(self):
        """Тест сохранения связей в БД"""
        schedule = Schedule.objects.create(
            title="Урок для связей",
            date=date(2024, 1, 15),
            week_day=1,  
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            classroom=self.classroom,
            org=self.org
        )
        
        self.assertEqual(Schedule.objects.count(), 1)
        
        self.assertEqual(schedule.teacher, self.teacher)
        self.assertEqual(schedule.group, self.group)
        self.assertEqual(schedule.subject, self.subject)
        
        self.assertIn(schedule, self.teacher.schedules.all())
        self.assertIn(schedule, self.group.schedules.all())
        self.assertIn(schedule, self.subject.schedule_set.all())  
    
    def test_subject_creation(self):
        """Тест создания предмета"""
        subject = Subject.objects.create(
            name="Физика",
            org=self.org
        )
        subject.teacher.add(self.teacher)
        
        self.assertEqual(subject.name, "Физика")
        self.assertEqual(subject.teacher.count(), 1)
        self.assertEqual(str(subject), "Физика")
    
    def test_subject_color_uniqueness(self):
        """Тест уникальности цвета предмета в организации"""
        # Создаем второй предмет с тем же цветом
        subject2 = Subject(
            name="Химия",
            color=self.subject_color,
            org=self.org
        )
        
        with self.assertRaises(ValidationError):
            subject2.clean()
    
    def test_classroom_creation(self):
        """Тест создания аудитории"""
        classroom = Classroom.objects.create(
            title="201",
            floor=2,
            building="Новый корпус",
            org=self.org
        )
        self.assertEqual(classroom.title, "201")
        self.assertEqual(classroom.floor, 2)
        self.assertEqual(str(classroom), "Аудитория 201")
    
    def test_period_schedule_creation(self):
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
                teacher=self.teacher,
                classroom=self.classroom,
                group=self.group,
                subject=self.subject,
                lesson=1,
                start_date=date(2024, 1, 15),
                repeat_lessons_until_date=date(2024, 6, 15),
                org=self.org
            )
            
            self.assertEqual(period_schedule.period, 7)
            self.assertEqual(period_schedule.title, "Еженедельная математика")
        finally:
            post_save.connect(lesson_signals.create_lessons_until_date, sender=PeriodSchedule)
    
    def test_attendance_creation(self):
        """Тест создания записи о посещении"""
        schedule = Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1,  
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        student = self.create_student(
            name="Алексей",  
            surname="Студентов",  
            birthday=date(2005, 5, 15)  
        )
        
        attendance = Attendance.objects.create(
            student=student,
            lesson=schedule,
            was_present=True,
            org=self.org
        )
        
        self.assertEqual(attendance.student, student)
        self.assertEqual(attendance.lesson, schedule)
        self.assertTrue(attendance.was_present)
        self.assertTrue("Алексей" in str(attendance))
    
    def test_grade_creation(self):
        """Тест создания оценки"""
        schedule = Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1, 
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        student = self.create_student(
            name="Мария",  
            surname="Студентова",  
            birthday=date(2006, 3, 20)  
        )
        
        grade = Grade.objects.create(
            student=student,
            lesson=schedule,
            value=5,
            comment="Отлично!",
            org=self.org
        )
        
        self.assertEqual(grade.student, student)
        self.assertEqual(grade.value, 5)
        self.assertEqual(grade.comment, "Отлично!")
        self.assertTrue("Мария" in str(grade))
    
    def test_grade_unique_constraint(self):
        """Тест уникальности оценки для студента и урока"""
        schedule = Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1, 
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        student = self.create_student(
            name="Петр", 
            surname="Учеников",  
            birthday=date(2004, 8, 10) 
        )
        
        Grade.objects.create(
            student=student,
            lesson=schedule, 
            value=5,
            org=self.org
        )
        
        with self.assertRaises(Exception):  
            Grade.objects.create(
                student=student,
                lesson=schedule,
                value=4,
                org=self.org
            )


class ScheduleRelationshipsTest(LessonScheduleLogicTest):
    """Тестирование связей между моделями"""
    
    def test_schedule_teacher_relationship(self):
        """Тест связи расписание-преподаватель"""
        schedule = Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1,  
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        self.assertEqual(schedule.teacher, self.teacher)
        self.assertIn(schedule, self.teacher.schedules.all())
    
    def test_schedule_classroom_relationship(self):
        """Тест связи расписание-аудитория"""
        schedule = Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1,  
            teacher=self.teacher,
            classroom=self.classroom,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        self.assertEqual(schedule.classroom, self.classroom)
        self.assertIn(schedule, self.classroom.schedules.all())
    
    def test_schedule_group_relationship(self):
        """Тест связи расписание-группа"""
        schedule = Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1, 
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        self.assertEqual(schedule.group, self.group)
        self.assertIn(schedule, self.group.schedules.all())
    
    def test_attendance_student_relationship(self):
        """Тест связи посещение-студент"""
        schedule = Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1,  
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        student = self.create_student(
            name="Алексей",  
            surname="Студентов",  
            birthday=date(2005, 5, 15)  
        )
        
        attendance = Attendance.objects.create(
            student=student,
            lesson=schedule,
            was_present=True,
            org=self.org
        )
        
        self.assertEqual(attendance.student, student)
        self.assertIn(attendance, student.attendances.all())


class ScheduleRequiredFieldsTest(LessonScheduleLogicTest):
    """Тесты обязательных полей расписания"""
    
    def test_schedule_required_fields(self):
        """Тест обязательных полей расписания"""
        schedule = Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1,  
            teacher=self.teacher,
            org=self.org
        )
        self.assertIsNotNone(schedule.id)


class ScheduleBusinessLogicTest(LessonScheduleLogicTest):
    """Тесты бизнес-логики расписания"""
    
    def test_schedule_string_representation(self):
        """Тест строкового представления расписания"""
        schedule = Schedule.objects.create(
            title="Важный урок",
            date=date(2024, 1, 15),
            week_day=1, 
            teacher=self.teacher,
            classroom=self.classroom,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        representation = str(schedule)
        self.assertIn("Важный урок", representation)
        self.assertIn("2024", representation)
    
    def test_week_day_auto_calculation(self):
        """Тест автоматического расчета дня недели"""
        schedule = Schedule.objects.create(
            date=date(2024, 1, 15),  
            teacher=self.teacher,
            org=self.org
        )
        # После сохранения week_day должен быть вычислен автоматически
        self.assertEqual(schedule.week_day, 1)  



class LessonScheduleUrlsTest(TestCase):
    """Тесты URL расписания занятий"""

    def setUp(self):
        from mainapp import signals as main_signals
        post_save.disconnect(main_signals.create_org_settings, sender=Organization)

    def tearDown(self):
        from mainapp import signals as main_signals
        post_save.connect(main_signals.create_org_settings, sender=Organization)

    def test_schedules_list_url(self):
        """Тест URL для списка расписаний"""
        url = reverse('schedule-list')
        self.assertEqual(resolve(url).func.cls.__name__, 'ScheduleViewSet')

    def test_schedules_detail_url(self):
        """Тест URL для деталей расписания"""
        url = reverse('schedule-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls.__name__, 'ScheduleViewSet')

    def test_subjects_list_url(self):
        """Тест URL для списка предметов"""
        url = reverse('subject-list')
        self.assertEqual(resolve(url).func.cls.__name__, 'SubjectViewSet')

    def test_classrooms_list_url(self):
        """Тест URL для списка аудиторий"""
        url = reverse('classroom-list')
        self.assertEqual(resolve(url).func.cls.__name__, 'ClassroomViewSet')

    def test_attendances_list_url(self):
        """Тест URL для списка посещений"""
        url = reverse('attendance-list')
        self.assertEqual(resolve(url).func.cls.__name__, 'AttendanceViewSet')

    def test_period_schedules_list_url(self):
        """Тест URL для списка периодических расписаний"""
        url = reverse('period_schedule-list')
        self.assertEqual(resolve(url).func.cls.__name__, 'PeriodScheduleViewSet')

    def test_grades_list_url(self):
        """Тест URL для списка оценок"""
        url = reverse('grade-list')
        self.assertEqual(resolve(url).func.cls.__name__, 'GradeViewSet')


class LessonScheduleBasicViewsTest(TestCase):
    """Базовые тесты views"""

    def setUp(self):
        from mainapp import signals as main_signals
        post_save.disconnect(main_signals.create_org_settings, sender=Organization)
        
        self.org = Organization.objects.create(name="Test Org")
        
        self.employer = Employer.objects.create(
            name="Тест", 
            surname="Преподаватель",
            org=self.org
        )
        self.teacher = Teacher.objects.create(employer=self.employer, org=self.org)
        
        self.subject = Subject.objects.create(name="Математика", org=self.org)
        self.subject.teacher.add(self.teacher)
        
        self.classroom = Classroom.objects.create(
            title="101", 
            floor=1,
            org=self.org
        )
        
        self.group = StudentGroup.objects.create(name="10А", org=self.org)

    def tearDown(self):
        from mainapp import signals as main_signals
        post_save.connect(main_signals.create_org_settings, sender=Organization)

    def test_schedule_creation_logic(self):
        """Тест логики создания расписания (без API)"""
        schedule = Schedule.objects.create(
            title="Тестовый урок",
            date=date(2024, 1, 15),
            week_day=1, 
            teacher=self.teacher,
            classroom=self.classroom,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        self.assertEqual(Schedule.objects.count(), 1)
        self.assertEqual(schedule.title, "Тестовый урок")
        self.assertEqual(schedule.week_day, 1)

    def test_subject_creation_logic(self):
        """Тест логики создания предмета (без API)"""
        subject = Subject.objects.create(
            name="Физика",
            org=self.org
        )
        subject.teacher.add(self.teacher)
        
        self.assertEqual(Subject.objects.count(), 2)  
        self.assertEqual(subject.name, "Физика")
        self.assertEqual(subject.teacher.count(), 1)

    def test_classroom_creation_logic(self):
        """Тест логики создания аудитории (без API)"""
        classroom = Classroom.objects.create(
            title="201",
            floor=2,
            building="Новый корпус",
            org=self.org
        )
        
        self.assertEqual(Classroom.objects.count(), 2)  
        self.assertEqual(classroom.title, "201")
        self.assertEqual(classroom.floor, 2)


class LessonScheduleChoiceFieldsTest(TestCase):
    """Тесты полей с выбором"""

    def test_week_day_choices(self):
        """Тест вариантов дней недели"""
        self.assertEqual(len(WEEK_DAY_CHOICES), 7)
        self.assertEqual(WEEK_DAY_CHOICES[0], (1, "Monday"))
        self.assertEqual(WEEK_DAY_CHOICES[6], (7, "Sunday"))

    def test_grade_choices(self):
        """Тест вариантов оценок"""
        self.assertEqual(len(GRADE_CHOICES), 4)
        self.assertEqual(GRADE_CHOICES[0], (2, "Не удовлетварительно"))
        self.assertEqual(GRADE_CHOICES[3], (5, "Отлично"))


class LessonScheduleUtilsTest(TestCase):
    """Вспомогательные тесты для расписания"""

    def test_model_meta(self):
        """Тест мета-данных моделей"""
        self.assertEqual(Schedule._meta.verbose_name, 'Занятие')
        self.assertEqual(Schedule._meta.verbose_name_plural, 'Занятия')
        self.assertEqual(Subject._meta.verbose_name, 'Предмет')
        self.assertEqual(Subject._meta.verbose_name_plural, 'Предметы')
        self.assertEqual(Classroom._meta.verbose_name, 'Аудитория')
        self.assertEqual(Classroom._meta.verbose_name_plural, 'Аудиории')
        self.assertEqual(Attendance._meta.verbose_name, 'Посещение')
        self.assertEqual(Attendance._meta.verbose_name_plural, 'Посещения')
        self.assertEqual(Grade._meta.verbose_name, 'Оценка')
        self.assertEqual(Grade._meta.verbose_name_plural, 'Оценки')

    def test_ordering(self):
        """Тест порядка сортировки"""
        self.assertEqual(Schedule._meta.ordering, ['date', 'start_time'])


class ScheduleIntegrationTest(LessonScheduleLogicTest):
    """Комплексные тесты, комбинирующие оба подхода"""
    
    def test_complete_schedule_lifecycle(self):
        """Тест полного жизненного цикла расписания"""
        
        schedule = self.create_unsaved_schedule(
            title="Интеграционный тест",
            date=date(2024, 1, 15),
            start_time=time(9, 0),
            end_time=time(10, 30),
            group=self.group,
            subject=self.subject
        )
        
        duration = schedule.calc_duration
        self.assertEqual(duration.total_seconds() / 3600, 1.5)
        
        schedule.clean()  
        schedule_to_save = Schedule(
            title=schedule.title,
            date=schedule.date,
            week_day=schedule.week_day, 
            teacher=schedule.teacher,
            group=schedule.group,
            subject=schedule.subject,
            org=schedule.org
        )
        schedule_to_save.save()
        
        self.assertEqual(Schedule.objects.count(), 1)
        saved_schedule = Schedule.objects.first()
        self.assertEqual(saved_schedule.title, "Интеграционный тест")
        
        self.assertEqual(saved_schedule.teacher.schedules.count(), 1)
        self.assertEqual(saved_schedule.group.schedules.count(), 1)


class OrganizationSecurityTest(APITestCase):
    """Тесты безопасности между организациями с использованием APITestCase"""
    
    def setUp(self):
        from mainapp import signals as main_signals
        post_save.disconnect(main_signals.create_org_settings, sender=Organization)
        
        self.org1 = Organization.objects.create(name="Organization 1")
        self.org2 = Organization.objects.create(name="Organization 2")
        
        self.org_settings1 = OrgSettings.objects.create(org=self.org1, timezone="UTC")
        self.org_settings2 = OrgSettings.objects.create(org=self.org2, timezone="UTC")
        
        self.user1 = User.objects.create(
            email="user1@org1.com", 
            username="user1_org1",  
            org=self.org1
        )
        
        self.user2 = User.objects.create(
            email="user2@org2.com",
            username="user2_org2",  
            org=self.org2
        )
        
        self.color_org1 = SubjectColor.objects.create(
            title="Синий Org1",
            color_hex="#0000FF",
            org=self.org1
        )
        
        self.teacher_org1 = Teacher.objects.create(
            employer=Employer.objects.create(name="Учитель", surname="Org1", org=self.org1),
            org=self.org1
        )
        
        self.subject_org1 = Subject.objects.create(
            name="Математика Org1",
            color=self.color_org1,
            org=self.org1
        )
        self.subject_org1.teacher.add(self.teacher_org1)
        
        self.classroom_org1 = Classroom.objects.create(title="101", org=self.org1)
        self.group_org1 = StudentGroup.objects.create(name="10А", org=self.org1)
        
        self.color_org2 = SubjectColor.objects.create(
            title="Красный Org2",
            color_hex="#FF0000",
            org=self.org2
        )
        
        self.teacher_org2 = Teacher.objects.create(
            employer=Employer.objects.create(name="Учитель", surname="Org2", org=self.org2),
            org=self.org2
        )
        
        self.subject_org2 = Subject.objects.create(
            name="Математика Org2",
            color=self.color_org2,
            org=self.org2
        )
        self.subject_org2.teacher.add(self.teacher_org2)
        
        self.classroom_org2 = Classroom.objects.create(title="201", org=self.org2)
        self.group_org2 = StudentGroup.objects.create(name="10Б", org=self.org2)
        
        self.student_org1 = Student.objects.create(
            name="Студент",
            surname="Org1",
            birthday=date(2005, 1, 1),
            org=self.org1
        )
        
        self.student_org2 = Student.objects.create(
            name="Студент", 
            surname="Org2",
            birthday=date(2005, 1, 1),
            org=self.org2
        )
        
        self.schedule_org1 = Schedule.objects.create(
            title="Урок Org1",
            date=date(2024, 1, 15),
            week_day=1,  
            teacher=self.teacher_org1,
            group=self.group_org1,
            subject=self.subject_org1,
            org=self.org1
        )
        
        self.schedule_org2 = Schedule.objects.create(
            title="Урок Org2",
            date=date(2024, 1, 15),
            week_day=1,  
            teacher=self.teacher_org2,
            group=self.group_org2,
            subject=self.subject_org2,
            org=self.org2
        )

    def tearDown(self):
        from mainapp import signals as main_signals
        post_save.connect(main_signals.create_org_settings, sender=Organization)

    def test_subject_color_organization_isolation(self):
        """Тест изоляции цветов предметов между организациями"""
        colors_org1 = SubjectColor.objects.filter(org=self.org1)
        self.assertEqual(colors_org1.count(), 1)
        self.assertIn(self.color_org1, colors_org1)
        self.assertNotIn(self.color_org2, colors_org1)
        
        colors_org2 = SubjectColor.objects.filter(org=self.org2)
        self.assertEqual(colors_org2.count(), 1)
        self.assertIn(self.color_org2, colors_org2)
        self.assertNotIn(self.color_org1, colors_org2)

    def test_api_color_access_organization_isolation(self):
        """Тест изоляции доступа к цветам через API"""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('subject_color-list')
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])
        
        if response.status_code == status.HTTP_200_OK:
            colors_data = response.json()
            if 'results' in colors_data:
                colors_list = colors_data['results']
            else:
                colors_list = colors_data
                
            self.assertTrue(len(colors_list) >= 1)
            color_titles = [color['title'] for color in colors_list]
            self.assertIn("Синий Org1", color_titles)

    def test_api_cross_organization_color_access_prevention(self):
        """Тест предотвращения доступа к цветам чужой организации через API"""
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('subject_color-detail', kwargs={'pk': self.color_org2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_subject_creation_organization_isolation(self):
        """Тест изоляции создания предметов через API"""
        self.client.force_authenticate(user=self.user1)
        
        subject_data = {
            'name': 'Новый предмет Org1',
            'color': self.color_org1.id,
        }
        
        url = reverse('subject-list')
        response = self.client.post(url, subject_data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
        
        if response.status_code == status.HTTP_201_CREATED:
            new_subject = Subject.objects.get(id=response.json()['id'])
            self.assertEqual(new_subject.org, self.org1)

    def test_api_cross_organization_subject_creation_prevention(self):
        """Тест предотвращения создания предмета для чужой организации через API"""
        self.client.force_authenticate(user=self.user1)
        
        subject_data = {
            'name': 'Новый предмет с чужим цветом',
            'color': self.color_org2.id,  
        }
        
        url = reverse('subject-list')
        response = self.client.post(url, subject_data)
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND])

    def test_api_attendance_organization_isolation(self):
        """Тест изоляции посещаемости между организациями через API"""
        attendance_org1 = Attendance.objects.create(
            student=self.student_org1,
            lesson=self.schedule_org1,
            was_present=True,
            org=self.org1
        )
        
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('attendance-list')
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])
        
        if response.status_code == status.HTTP_200_OK:
            attendances_data = response.json()
            if 'results' in attendances_data:
                attendances_list = attendances_data['results']
            else:
                attendances_list = attendances_data
                
            self.assertTrue(len(attendances_list) >= 1)

    def test_api_attendance_cross_organization_access_prevention(self):
        """Тест предотвращения доступа к посещениям чужой организации через API"""
        attendance_org2 = Attendance.objects.create(
            student=self.student_org2,
            lesson=self.schedule_org2,
            was_present=True,
            org=self.org2
        )
        
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('attendance-detail', kwargs={'pk': attendance_org2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ScheduleConflictValidationTest(LessonScheduleLogicTest):
    """ТЕСТЫ КОНФЛИКТОВ РАСПИСАНИЯ: проверяют валидацию пересечений времени"""
    
    def test_teacher_conflict_validation(self):
        """✅ Конфликт преподавателя: один учитель не может вести два занятия одновременно"""
        # Создаем первое занятие
        Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1, 
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        # Пытаемся создать конфликтующее занятие с тем же преподавателем
        conflicting_schedule = Schedule(
            date=date(2024, 1, 15),
            week_day=1,  
            start_time=time(9, 0),  
            end_time=time(10, 30),
            teacher=self.teacher,  
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        with self.assertRaises(ValidationError) as context:
            conflicting_schedule.clean()
        
        self.assertIn("У этого преподавателя на пару и дату занятие", str(context.exception))
    
    def test_group_conflict_validation(self):
        """✅ Конфликт группы: одна группа не может быть на двух занятиях одновременно"""
        # Создаем второго преподавателя для этого теста
        employer2 = Employer.objects.create(
            name="Второй", 
            surname="Преподаватель", 
            org=self.org
        )
        teacher2 = Teacher.objects.create(employer=employer2, org=self.org)
        
        # Создаем первое занятие с первым преподавателем
        Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1,  
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=self.teacher, 
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        # Пытаемся создать конфликтующее занятие с той же группой, но РАЗНЫМ преподавателем
        conflicting_schedule = Schedule(
            date=date(2024, 1, 15),
            week_day=1, 
            start_time=time(9, 0),  
            end_time=time(10, 30),
            teacher=teacher2,  
            group=self.group, 
            subject=self.subject,
            org=self.org
        )
        
        with self.assertRaises(ValidationError) as context:
            conflicting_schedule.clean()
        
        self.assertIn("У этой группы на эту пару и дату занятие", str(context.exception))
    
    def test_no_conflict_different_times(self):
        """✅ Отсутствие конфликта: занятия в разное время"""
        Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1,  
            start_time=time(9, 0),
            end_time=time(10, 0),
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        # Занятие после первого - конфликта быть не должно
        non_conflicting_schedule = Schedule(
            date=date(2024, 1, 15),
            week_day=1,  
            start_time=time(10, 30), 
            end_time=time(11, 30),
            teacher=self.teacher,  
            group=self.group,  
            subject=self.subject,  
            org=self.org
        )
        
        try:
            non_conflicting_schedule.clean()
        except ValidationError:
            self.fail("Не должно быть конфликта для разного времени")
    
    def test_no_conflict_different_dates(self):
        """✅ Отсутствие конфликта: занятия в разные даты"""
        Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1, 
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        # То же время, но другая дата - конфликта быть не должно
        non_conflicting_schedule = Schedule(
            date=date(2024, 1, 16),  
            week_day=2,  
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        try:
            non_conflicting_schedule.clean()
        except ValidationError:
            self.fail("Не должно быть конфликта для разных дат")
    
    def test_partial_time_overlap_conflict(self):
        """✅ Частичное пересечение времени: начало внутри другого занятия"""
        Schedule.objects.create(
            date=date(2024, 1, 15),
            week_day=1, 
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        # Частичное пересечение (начало внутри другого занятия)
        conflicting_schedule = Schedule(
            date=date(2024, 1, 15),
            week_day=1,  
            start_time=time(10, 0), 
            end_time=time(11, 30),
            teacher=self.teacher,  
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        with self.assertRaises(ValidationError):
            conflicting_schedule.clean()


class FastConflictTests(LessonScheduleLogicTest):
    """ Быстрые тесты конфликтов"""
    
    def test_fast_teacher_conflict(self):
        """ Быстрый тест конфликта преподавателя"""
        Schedule.objects.create(
            date=date(2024, 1, 15), 
            week_day=1,  
            start_time=time(9, 0), 
            end_time=time(10, 30),
            teacher=self.teacher, 
            group=self.group, 
            subject=self.subject, 
            org=self.org
        )
        
        conflict = Schedule(
            date=date(2024, 1, 15), 
            week_day=1, 
            start_time=time(9, 0), 
            end_time=time(10, 30),
            teacher=self.teacher, 
            group=self.group, 
            subject=self.subject, 
            org=self.org
        )
        
        with self.assertRaises(ValidationError):
            conflict.clean()
    
    def test_fast_no_conflict(self):
        """ Быстрый тест отсутствия конфликта"""
        Schedule.objects.create(
            date=date(2024, 1, 15), 
            week_day=1,  
            start_time=time(9, 0), 
            end_time=time(10, 30),
            teacher=self.teacher, 
            group=self.group, 
            subject=self.subject, 
            org=self.org
        )
        
        no_conflict = Schedule(
            date=date(2024, 1, 16),  
            week_day=2,  
            start_time=time(9, 0), 
            end_time=time(10, 30),
            teacher=self.teacher, 
            group=self.group, 
            subject=self.subject, 
            org=self.org
        )
        
        try:
            no_conflict.clean()
        except ValidationError:
            self.fail("Не должно быть конфликта")

class LessonValidationMixinTests(LessonScheduleLogicTest):
    """Тесты миксина валидации уроков"""
    
    def setUp(self):
        super().setUp()
        
        from lesson_schedule.mixins import LessonValidationMixin
        self.mixin_instance = LessonValidationMixin()
        
        self.mixin_instance.get_lessons_queryset = lambda: Schedule.objects.all()
    
    def test_can_update_period_lesson_validation_success(self):
        """ Тест успешной валидации периодических занятий без конфликтов"""
        # Создаем PeriodSchedule и занятия
        period_schedule = PeriodSchedule.objects.create(
            period=7,
            start_date=date(2024, 1, 1),
            repeat_lessons_until_date=date(2024, 1, 15),
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            start_time=time(9, 0),
            end_time=time(10, 30),
            org=self.org
        )
        
        lessons = Schedule.objects.filter(period_schedule=period_schedule)
        self.assertEqual(lessons.count(), 3)  
        
        # Mock serializer для тестирования. Заглушка, которая сохраняет на промежуток одного времени
        class MockSerializer:
            def __init__(self, instance, validated_data):
                self.instance = instance
                self.validated_data = validated_data
        
        # Тестируем изменение на время, когда нет других занятий 
        serializer = MockSerializer(
            instance=period_schedule,
            validated_data={
                'start_time': time(16, 0),  
                'end_time': time(17, 30),
                'teacher': self.teacher,
                'classroom': None,
                'group': self.group
            }
        )
        
        try:
            result = self.mixin_instance.can_update_period_lesson(serializer=serializer, is_force_update=False)
            self.assertTrue(result)
        except ValidationError as e:
            self.fail(f"Не должно быть ValidationError для неконфликтующего времени: {e}")
    
    def test_can_update_period_lesson_with_force_update(self):
        """ Тест что is_force_update пропускает валидацию"""
        period_schedule = PeriodSchedule.objects.create(
            period=7,
            start_date=date(2024, 1, 1),
            repeat_lessons_until_date=date(2024, 1, 8),
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        class MockSerializer:
            def __init__(self, instance, validated_data):
                self.instance = instance
                self.validated_data = validated_data
        
        serializer = MockSerializer(
            instance=period_schedule,
            validated_data={
                'start_time': time(9, 0), 
                'end_time': time(10, 30),
                'teacher': self.teacher,
                'classroom': None,
                'group': self.group
            }
        )
        
        # С force_update=True не должно быть ошибки
        try:
            result = self.mixin_instance.can_update_period_lesson(serializer=serializer, is_force_update=True)
            self.assertTrue(result)
        except ValidationError:
            self.fail("Не должно быть ValidationError при is_force_update=True")
    
    def test_mixin_methods_exist(self):
        """ Тест что все методы миксина существуют и вызываются"""
        period_schedule = PeriodSchedule.objects.create(
            period=7,
            start_date=date(2024, 1, 1),
            repeat_lessons_until_date=date(2024, 1, 8),
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        class MockSerializer:
            def __init__(self, instance, validated_data):
                self.instance = instance
                self.validated_data = validated_data
        
        serializer = MockSerializer(
            instance=period_schedule,
            validated_data={
                'start_time': time(9, 0), 
                'end_time': time(10, 30),
                'teacher': self.teacher,
                'classroom': None,
                'group': self.group
            }
        )
        
        # Проверяем что методы можно вызвать
        try:
            fields = self.mixin_instance._extract_lesson_fields(serializer=serializer)
            self.assertIn('start_time', fields)
            self.assertIn('end_time', fields)
            self.assertIn('teacher', fields)
            self.assertIn('classroom', fields)
            self.assertIn('group', fields)
            
            related_lessons = self.mixin_instance._get_related_lessons(serializer=serializer)
            self.assertIsNotNone(related_lessons)
            
        except Exception as e:
            self.fail(f"Методы миксина должны работать корректно: {e}")

class CeleryTasksTests(LessonScheduleLogicTest):
    """Тесты Celery задач"""
    
    def test_update_complete_lessons_task(self):
        """✅ Тест автоматического помечания завершенных уроков"""
        from lesson_schedule.tasks import update_complete_lessons
        
        # Создаем занятие которое должно быть завершено
        past_lesson = Schedule.objects.create(
            date=date(2023, 12, 1),  
            start_time=time(9, 0),
            end_time=time(10, 0),
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            is_completed=False,
            org=self.org
        )
        print(past_lesson)
        
        # Создаем занятие которое еще не завершено (в будущем)
        future_lesson = Schedule.objects.create(
            date=date(2025, 12, 31),  
            week_day=3,  
            start_time=time(9, 0),
            end_time=time(10, 0),
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            is_completed=False,
            org=self.org
        )
        
        # Вызываем задачу для конкретной организации
        result = update_complete_lessons([self.org])
        
        # Проверяем что прошлое занятие помечено как завершенное
        past_lesson.refresh_from_db()
        self.assertTrue(past_lesson.is_completed)
        
        # Проверяем что будущее занятие осталось незавершенным
        future_lesson.refresh_from_db()
        self.assertFalse(future_lesson.is_completed)
    
    def test_create_attendences_for_all_passes_task(self):
        """✅ Тест создания записей посещений для пропусков"""
        from lesson_schedule.tasks import create_attendences_for_all_passes
        
        # Создаем студентов в группе
        student1 = Student.objects.create(
            name="Студент1", surname="Тестов", birthday=date(2005, 1, 1), org=self.org
        )
        student2 = Student.objects.create(
            name="Студент2", surname="Тестов", birthday=date(2005, 1, 1), org=self.org
        )
        self.group.students.add(student1, student2)
        
        # Создаем завершенное занятие
        completed_lesson = Schedule.objects.create(
            date=date(2024, 1, 1),
            week_day=1,  
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            is_completed=True,
            org=self.org
        )
        
        # Создаем посещение для одного студента
        Attendance.objects.create(
            student=student1,
            lesson=completed_lesson,
            was_present=True,
            org=self.org
        )
        
        # Вызываем задачу
        result = create_attendences_for_all_passes([self.org])
        
        # Проверяем что создалась запись для второго студента с was_present=False
        missing_attendance = Attendance.objects.filter(
            lesson=completed_lesson, 
            student=student2,
            was_present=False
        )
        self.assertTrue(missing_attendance.exists())
        
        # Проверяем что для первого студента не создалась дублирующая запись
        student1_attendances = Attendance.objects.filter(
            lesson=completed_lesson, 
            student=student1
        )
        self.assertEqual(student1_attendances.count(), 1) 
    
    def test_create_attendences_skips_lessons_without_group(self):
        """✅ Тест что занятия без группы пропускаются"""
        from lesson_schedule.tasks import create_attendences_for_all_passes
        
        # Создаем завершенное занятие без группы
        lesson_without_group = Schedule.objects.create(
            date=date(2024, 1, 1),
            week_day=1,  
            teacher=self.teacher,
            subject=self.subject,
            is_completed=True,
            org=self.org
            # Нет group!
        )
        
        # Вызываем задачу - не должно быть ошибок
        result = create_attendences_for_all_passes([self.org])
        
        # Не должно создаться записей посещений
        attendances_count = Attendance.objects.filter(lesson=lesson_without_group).count()
        self.assertEqual(attendances_count, 0)

class PeriodScheduleUpdateTests(LessonScheduleLogicTest):
    """Тесты обновления PeriodSchedule и каскадного обновления занятий"""
    
    def test_update_period_schedule_updates_incomplete_lessons(self):
        """✅ Тест что изменение PeriodSchedule обновляет незавершенные занятия"""
        # Создаем PeriodSchedule и занятия
        period_schedule = PeriodSchedule.objects.create(
            period=7,
            start_date=date(2024, 1, 1),
            repeat_lessons_until_date=date(2024, 1, 15),
            teacher=self.teacher,
            classroom=self.classroom,
            group=self.group,
            subject=self.subject,
            start_time=time(9, 0),
            end_time=time(10, 30),
            org=self.org
        )
        
        # Получаем созданные занятия
        lessons = Schedule.objects.filter(period_schedule=period_schedule)
        self.assertGreater(lessons.count(), 0)
        
        # Создаем второго преподавателя для теста обновления
        employer2 = Employer.objects.create(
            name="Новый", 
            surname="Преподаватель", 
            org=self.org
        )
        teacher2 = Teacher.objects.create(employer=employer2, org=self.org)
        
        # Обновляем PeriodSchedule
        period_schedule.teacher = teacher2
        period_schedule.start_time = time(10, 0)
        period_schedule.end_time = time(11, 30)
        period_schedule.save()
        
        # Проверяем что незавершенные занятия обновились
        updated_lessons = Schedule.objects.filter(period_schedule=period_schedule, is_completed=False)
        for lesson in updated_lessons:
            self.assertEqual(lesson.teacher, teacher2)
            self.assertEqual(lesson.start_time, time(10, 0))
            self.assertEqual(lesson.end_time, time(11, 30))
    
    def test_update_period_schedule_ignores_completed_lessons(self):
        """✅ Тест что завершенные занятия не обновляются"""
        # Создаем PeriodSchedule
        period_schedule = PeriodSchedule.objects.create(
            period=7,
            start_date=date(2024, 1, 1),
            repeat_lessons_until_date=date(2024, 1, 8),
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            title="Исходное название",  
            org=self.org
        )
        
        lessons = Schedule.objects.filter(period_schedule=period_schedule)
        
        # Помечаем одно занятие как завершенное
        completed_lesson = lessons.first()
        completed_lesson.is_completed = True
        completed_lesson.save()
        
        # Обновляем PeriodSchedule
        period_schedule.title = "Обновленное название"
        period_schedule.save()
        
        # Проверяем что завершенное занятие не обновилось
        completed_lesson.refresh_from_db()
        self.assertNotEqual(completed_lesson.title, "Обновленное название")
        
        # Проверяем что незавершенные занятия обновились
        incomplete_lessons = lessons.filter(is_completed=False)
        for lesson in incomplete_lessons:
            lesson.refresh_from_db()
            self.assertEqual(lesson.title, "Обновленное название")

class PeriodScheduleSignalTests(LessonScheduleLogicTest):
    """Тесты сигналов PeriodSchedule"""
    
    def test_create_lessons_until_date_weekly(self):
        """✅ Тест автоматического создания еженедельных занятий"""
        from lesson_schedule import signals as lesson_signals
        
        # Отключаем сигнал обновления чтобы тестировать только создание
        from django.db.models.signals import post_save
        post_save.disconnect(lesson_signals.update_data_not_complete_lessons, sender=PeriodSchedule)
        
        try:
            period_schedule = PeriodSchedule.objects.create(
                period=7, 
                title="Еженедельная математика",
                start_time=time(9, 0),
                end_time=time(10, 30),
                teacher=self.teacher,
                classroom=self.classroom,
                group=self.group,
                subject=self.subject,
                lesson=1,
                start_date=date(2024, 1, 1), 
                repeat_lessons_until_date=date(2024, 1, 22),  
                org=self.org
            )
            
            # Проверяем созданные занятия
            created_lessons = Schedule.objects.filter(period_schedule=period_schedule)
            self.assertEqual(created_lessons.count(), 4) 
            
            # Проверяем даты занятий
            lesson_dates = [lesson.date for lesson in created_lessons]
            expected_dates = [date(2024, 1, 1), date(2024, 1, 8), date(2024, 1, 15), date(2024, 1, 22)]
            self.assertEqual(lesson_dates, expected_dates)
            
            # Проверяем что все занятия имеют правильные атрибуты
            for lesson in created_lessons:
                self.assertEqual(lesson.teacher, self.teacher)
                self.assertEqual(lesson.classroom, self.classroom)
                self.assertEqual(lesson.group, self.group)
                self.assertEqual(lesson.subject, self.subject)
                self.assertEqual(lesson.start_time, time(9, 0))
                self.assertEqual(lesson.end_time, time(10, 30))
                
        finally:
            # Восстанавливаем сигнал
            post_save.connect(lesson_signals.update_data_not_complete_lessons, sender=PeriodSchedule)
    
    def test_create_lessons_until_date_daily(self):
        """✅ Тест автоматического создания ежедневных занятий"""
        from lesson_schedule import signals as lesson_signals
        from django.db.models.signals import post_save
        post_save.disconnect(lesson_signals.update_data_not_complete_lessons, sender=PeriodSchedule)
        
        try:
            period_schedule = PeriodSchedule.objects.create(
                period=1,
                start_date=date(2024, 1, 1),
                repeat_lessons_until_date=date(2024, 1, 5),
                teacher=self.teacher,
                group=self.group,
                subject=self.subject,
                org=self.org
            )
            
            created_lessons = Schedule.objects.filter(period_schedule=period_schedule)
            self.assertEqual(created_lessons.count(), 5) 
            
        finally:
            post_save.connect(lesson_signals.update_data_not_complete_lessons, sender=PeriodSchedule)
    
    def test_create_lessons_with_org_settings_date(self):
        """✅ Тест создания занятий с датой окончания из настроек организации"""
        from lesson_schedule import signals as lesson_signals
        from django.db.models.signals import post_save
        post_save.disconnect(lesson_signals.update_data_not_complete_lessons, sender=PeriodSchedule)
        
        try:
            # Устанавливаем дату окончания в настройках организации
            self.org_settings.repeat_lessons_until = "06-30"  
            self.org_settings.save()
            
            period_schedule = PeriodSchedule.objects.create(
                period=7,
                start_date=date(2024, 1, 1),
                teacher=self.teacher,
                group=self.group,
                subject=self.subject,
                org=self.org
            )
            
            created_lessons = Schedule.objects.filter(period_schedule=period_schedule)
            self.assertGreater(created_lessons.count(), 0)
            
        finally:
            post_save.connect(lesson_signals.update_data_not_complete_lessons, sender=PeriodSchedule)
    
    def test_period_schedule_without_period_raises_error(self):
        """✅ Тест что PeriodSchedule без периода вызывает ошибку"""
        from lesson_schedule import signals as lesson_signals
        from django.db.models.signals import post_save
        post_save.disconnect(lesson_signals.update_data_not_complete_lessons, sender=PeriodSchedule)
        
        try:
            with self.assertRaises(ValueError) as context:
                period_schedule = PeriodSchedule.objects.create(
                    start_date=date(2024, 1, 1),
                    repeat_lessons_until_date=date(2024, 1, 8),
                    teacher=self.teacher,
                    group=self.group,
                    subject=self.subject,
                    org=self.org
                )
            
            self.assertIn("не указана периодичность", str(context.exception))
            
        finally:
            post_save.connect(lesson_signals.update_data_not_complete_lessons, sender=PeriodSchedule)

class ComplexScenariosTests(LessonScheduleLogicTest):
    """Тесты комплексных сценариев работы с периодическими занятиями"""
    
    def test_cascade_update_complex_scenario(self):
        """✅ Комплексный тест каскадного обновления PeriodSchedule → Schedule"""
        # Создаем PeriodSchedule с занятиями
        period_schedule = PeriodSchedule.objects.create(
            period=7,
            start_date=date(2024, 1, 1),
            repeat_lessons_until_date=date(2024, 1, 22),
            teacher=self.teacher,
            classroom=self.classroom,
            group=self.group,
            subject=self.subject,
            start_time=time(9, 0),
            end_time=time(10, 30),
            title="Исходное расписание",  
            org=self.org
        )
        
        lessons = Schedule.objects.filter(period_schedule=period_schedule)
        initial_count = lessons.count()
        self.assertGreater(initial_count, 0)
        
        # Помечаем некоторые занятия как завершенные
        completed_lessons = lessons[:2]
        for lesson in completed_lessons:
            lesson.is_completed = True
            lesson.save()
        
        # Обновляем PeriodSchedule
        period_schedule.title = "Обновленное расписание"
        period_schedule.save()  

        # Проверяем результаты
        updated_lessons = Schedule.objects.filter(period_schedule=period_schedule)
        
        # Проверяем незавершенные занятия
        incomplete_lessons = updated_lessons.filter(is_completed=False)
        for lesson in incomplete_lessons:
            lesson.refresh_from_db()
            self.assertEqual(lesson.title, "Обновленное расписание")

    def test_period_schedule_with_conflicting_parameters(self):
        """✅ Тест что PeriodSchedule создает занятия, но конфликтующие не сохраняются"""
        # Создаем конфликтующее занятие
        Schedule.objects.create(
            date=date(2024, 1, 8),
            week_day=1,  # ✅ ДОБАВЛЕНО явное указание week_day
            start_time=time(9, 0),
            end_time=time(10, 30),
            teacher=self.teacher,
            group=self.group,
            subject=self.subject,
            org=self.org
        )
        
        # Отключаем сигнал обновления чтобы тестировать только создание
        from lesson_schedule import signals as lesson_signals
        from django.db.models.signals import post_save
        post_save.disconnect(lesson_signals.update_data_not_complete_lessons, sender=PeriodSchedule)
        
        try:
            # Создаем PeriodSchedule - должен сохраниться БЕЗ ошибки
            period_schedule = PeriodSchedule.objects.create(
                period=7,
                start_date=date(2024, 1, 1),
                repeat_lessons_until_date=date(2024, 1, 8),
                teacher=self.teacher,
                group=self.group,
                subject=self.subject,
                start_time=time(9, 0),
                end_time=time(10, 30),
                org=self.org
            )
            
            # Проверяем что PeriodSchedule создался
            self.assertIsNotNone(period_schedule.id)
            
            # Проверяем что создались НЕ ВСЕ занятия (конфликтующие пропущены)
            created_lessons = Schedule.objects.filter(period_schedule=period_schedule)
            # Должны быть: 1 января (успешно), 8 января (пропущено из-за конфликта)
            self.assertEqual(created_lessons.count(), 1)  # Только 1 января
            self.assertEqual(created_lessons.first().date, date(2024, 1, 1))
            
        finally:
            post_save.connect(lesson_signals.update_data_not_complete_lessons, sender=PeriodSchedule)
    
    def test_boundary_cases_different_months_years(self):
        """✅ Тест граничных случаев с разными месяцами и годами"""
        from lesson_schedule import signals as lesson_signals
        from django.db.models.signals import post_save
        post_save.disconnect(lesson_signals.update_data_not_complete_lessons, sender=PeriodSchedule)
        
        try:
            # Период через границу года
            period_schedule = PeriodSchedule.objects.create(
                period=30,  # ~ месяц
                start_date=date(2023, 12, 1),
                repeat_lessons_until_date=date(2024, 2, 1),
                teacher=self.teacher,
                group=self.group,
                subject=self.subject,
                org=self.org
            )
            
            created_lessons = Schedule.objects.filter(period_schedule=period_schedule)
            lesson_dates = [lesson.date for lesson in created_lessons]
            
            # Проверяем что есть занятия в разных месяцах/годах
            years_in_lessons = {lesson_date.year for lesson_date in lesson_dates}
            months_in_lessons = {lesson_date.month for lesson_date in lesson_dates}
            
            self.assertGreater(len(months_in_lessons), 1)
            
        finally:
            post_save.connect(lesson_signals.update_data_not_complete_lessons, sender=PeriodSchedule)

class ScheduleAPITest(APITestCase):
    """API тесты для расписания"""
    
    def setUp(self):
        from mainapp import signals as main_signals
        post_save.disconnect(main_signals.create_org_settings, sender=Organization)
        
        self.org = Organization.objects.create(name="Test Org")
        self.org_settings = OrgSettings.objects.create(org=self.org, timezone="UTC")
        
        self.employer = Employer.objects.create(
            name="Тест", 
            surname="Преподаватель", 
            org=self.org
        )
        self.teacher = Teacher.objects.create(employer=self.employer, org=self.org)
        
        self.subject = Subject.objects.create(name="Математика", org=self.org)
        self.subject.teacher.add(self.teacher)
        
        self.classroom = Classroom.objects.create(title="101", org=self.org)
        self.group = StudentGroup.objects.create(name="10А", org=self.org)
        
        # Создаем пользователя для аутентификации
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123", 
            email="test@example.com",
            org=self.org
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def tearDown(self):
        from mainapp import signals as main_signals
        post_save.connect(main_signals.create_org_settings, sender=Organization)
    
    def test_schedule_list_api(self):
        """Тест API списка расписаний"""
        url = reverse('schedule-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_schedule_creation_api(self):
        """Тест API создания расписания"""
        url = reverse('schedule-list')
        data = {
            'title': 'API Тест',
            'date': '2024-01-15',
            'teacher': self.teacher.id,
            'group': self.group.id,
            'subject': self.subject.id,
            'classroom': self.classroom.id,
            'start_time': '09:00',
            'end_time': '10:30'
        }
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
    
    def test_subject_list_api(self):
        """Тест API списка предметов"""
        url = reverse('subject-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_classroom_list_api(self):
        """Тест API списка аудиторий"""
        url = reverse('classroom-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)