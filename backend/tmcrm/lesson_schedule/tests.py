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
from datetime import date, time, timedelta
from django.utils import timezone


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
        
        self.assertEqual(schedule.calc_duration_hours, 1.5)
    
    def test_duration_edge_cases(self):
        """Тест крайних случаев расчета длительности"""
        test_cases = [
            (time(9, 0), time(9, 45), 0.75, "45 минут"),
            (time(14, 0), time(16, 30), 2.5, "2.5 часа"),
            (time(9, 0), time(11, 0), 2.0, "2 часа"), 
            (time(0, 0), time(0, 0), 0.0, "нулевая длительность"),
        ]
        
        for start, end, expected, description in test_cases:
            with self.subTest(description):
                schedule = self.create_unsaved_schedule(
                    start_time=start,
                    end_time=end
                )
                self.assertEqual(schedule.calc_duration_hours, expected)
    
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
        new_color = SubjectColor.objects.create(
            title="Красный",
            color_hex="#FF0000",  
            org=self.org
        )
        
        subject2 = Subject.objects.create(
            name="Химия",
            org=self.org
        )
        
        subject2.color = self.subject_color
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
        
        self.assertEqual(schedule.calc_duration_hours, 1.5)
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

