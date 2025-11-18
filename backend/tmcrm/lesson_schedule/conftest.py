import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from datetime import date, time

from lesson_schedule.models import Schedule, Subject, Classroom, PeriodSchedule, Attendance, Grade
from students.models import StudentGroup, Student
from employers.models import Teacher, Employer
from mainapp.models import Organization, User, SubjectColor, OrgSettings

User = get_user_model()


@pytest.fixture
def api_client():
    """Базовая фикстура API клиента"""
    return APIClient()


@pytest.fixture(autouse=True)
def disable_org_settings_signal():
    """Автоматически отключает сигнал создания настроек организации для всех тестов"""
    from mainapp import signals as main_signals
    from django.db.models.signals import post_save
    
    post_save.disconnect(main_signals.create_org_settings, sender=Organization)
    yield
    post_save.connect(main_signals.create_org_settings, sender=Organization)


@pytest.fixture
def organization(db):
    """Фикстура организации"""
    org = Organization.objects.create(name="Test Org")
    OrgSettings.objects.create(
        org=org,
        timezone="UTC",
        repeat_lessons_until="06-30"
    )
    return org


@pytest.fixture
def organization2(db):
    """Фикстура второй организации"""
    org = Organization.objects.create(name="Organization 2")
    OrgSettings.objects.create(org=org, timezone="UTC")
    return org


@pytest.fixture
def user(organization):
    """Фикстура пользователя"""
    return User.objects.create_user(
        username="testuser",
        password="testpass123", 
        email="test@example.com",
        org=organization,
    )


@pytest.fixture
def user2(organization2):
    """Фикстура пользователя второй организации"""
    return User.objects.create(
        email="user2@org2.com",
        username="user2_org2",  
        org=organization2
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Фикстура аутентифицированного API клиента"""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def employer(organization):
    """Фикстура работника"""
    return Employer.objects.create(
        name="Тест", 
        surname="Преподаватель", 
        org=organization
    )


@pytest.fixture
def employer2(organization):
    """Фикстура второго работника"""
    return Employer.objects.create(
        name="Второй", 
        surname="Преподаватель", 
        org=organization
    )


@pytest.fixture
def teacher(organization, employer):
    """Фикстура преподавателя"""
    return Teacher.objects.create(employer=employer, org=organization)


@pytest.fixture
def teacher2(organization, employer2):
    """Фикстура второго преподавателя"""
    return Teacher.objects.create(employer=employer2, org=organization)


@pytest.fixture
def teacher_org2(organization2):
    """Фикстура преподавателя второй организации"""
    employer = Employer.objects.create(
        name="Учитель", 
        surname="Org2", 
        org=organization2
    )
    return Teacher.objects.create(employer=employer, org=organization2)


@pytest.fixture
def subject_color(organization):
    """Фикстура цвета предмета"""
    return SubjectColor.objects.create(
        title="Синий",
        color_hex="#0000FF",  
        org=organization
    )


@pytest.fixture
def subject_color2(organization):
    """Фикстура второго цвета предмета для той же организации"""
    return SubjectColor.objects.create(
        title="Красный",
        color_hex="#FF0000",  
        org=organization
    )


@pytest.fixture
def subject_color_org2(organization2):
    """Фикстура цвета предмета второй организации"""
    return SubjectColor.objects.create(
        title="Красный Org2",
        color_hex="#FF0000",
        org=organization2
    )


@pytest.fixture
def subject(organization, teacher, subject_color):
    """Фикстура предмета"""
    subject = Subject.objects.create(
        name="Математика", 
        color=subject_color,
        org=organization
    )
    subject.teacher.add(teacher)
    return subject


@pytest.fixture
def subject2(organization, teacher2, subject_color2):
    """Фикстура второго предмета"""
    subject = Subject.objects.create(
        name="Физика", 
        color=subject_color2,
        org=organization
    )
    subject.teacher.add(teacher2)
    return subject


@pytest.fixture
def subject_org2(organization2, teacher_org2, subject_color_org2):
    """Фикстура предмета второй организации"""
    subject = Subject.objects.create(
        name="Математика Org2",
        color=subject_color_org2,
        org=organization2
    )
    subject.teacher.add(teacher_org2)
    return subject


@pytest.fixture
def classroom(organization):
    """Фикстура аудитории"""
    return Classroom.objects.create(title="101", org=organization)


@pytest.fixture
def classroom2(organization):
    """Фикстура второй аудитории"""
    return Classroom.objects.create(title="102", org=organization)


@pytest.fixture
def classroom_org2(organization2):
    """Фикстура аудитории второй организации"""
    return Classroom.objects.create(title="201", org=organization2)


@pytest.fixture
def student_group(organization):
    """Фикстура группы студентов"""
    group = StudentGroup.objects.create(name="10А", org=organization)
    return group


@pytest.fixture
def student_group2(organization):
    """Фикстура второй группы студентов"""
    return StudentGroup.objects.create(name="10Б", org=organization)


@pytest.fixture
def student_group_org2(organization2):
    """Фикстура группы студентов второй организации"""
    return StudentGroup.objects.create(name="10Б", org=organization2)


@pytest.fixture
def student(organization, student_group):
    """Фикстура студента"""
    student = Student.objects.create(
        name="Иван",
        surname="Тестов",
        birthday=date(2005, 1, 1),
        org=organization
    )
    student_group.students.add(student)
    return student


@pytest.fixture
def student2(organization, student_group):
    """Фикстура второго студента"""
    student = Student.objects.create(
        name="Петр",
        surname="Учеников",
        birthday=date(2005, 1, 1),
        org=organization
    )
    student_group.students.add(student)
    return student


@pytest.fixture
def student_org1(organization):
    """Фикстура студента первой организации"""
    return Student.objects.create(
        name="Студент",
        surname="Org1",
        birthday=date(2005, 1, 1),
        org=organization
    )


@pytest.fixture
def student_org2(organization2):
    """Фикстура студента второй организации"""
    return Student.objects.create(
        name="Студент", 
        surname="Org2",
        birthday=date(2005, 1, 1),
        org=organization2
    )


@pytest.fixture
def schedule(organization, teacher, student_group, subject, classroom):
    """Фикстура занятия"""
    return Schedule.objects.create(
        title="Тестовое занятие",
        date=date(2024, 1, 15),
        week_day=1,
        start_time=time(9, 0),
        end_time=time(10, 30),
        teacher=teacher,
        group=student_group,
        subject=subject,
        classroom=classroom,
        org=organization
    )


@pytest.fixture
def schedule_org1(organization, teacher, student_group, subject):
    """Фикстура занятия первой организации"""
    return Schedule.objects.create(
        title="Урок Org1",
        date=date(2024, 1, 15),
        week_day=1,  
        teacher=teacher,
        group=student_group,
        subject=subject,
        org=organization
    )


@pytest.fixture
def schedule_org2(organization2, teacher_org2, student_group_org2, subject_org2):
    """Фикстура занятия второй организации"""
    return Schedule.objects.create(
        title="Урок Org2",
        date=date(2024, 1, 15),
        week_day=1,  
        teacher=teacher_org2,
        group=student_group_org2,
        subject=subject_org2,
        org=organization2
    )


@pytest.fixture
def attendance(organization, schedule, student):
    """Фикстура посещения"""
    return Attendance.objects.create(
        student=student,
        lesson=schedule,
        was_present=True,
        org=organization
    )


@pytest.fixture
def attendance_org2(organization2, schedule_org2, student_org2):
    """Фикстура посещения второй организации"""
    return Attendance.objects.create(
        student=student_org2,
        lesson=schedule_org2,
        was_present=True,
        org=organization2
    )


@pytest.fixture
def grade(organization, schedule, student):
    """Фикстура оценки"""
    return Grade.objects.create(
        student=student,
        lesson=schedule,
        value=5,
        org=organization
    )


@pytest.fixture
def period_schedule(organization, teacher, student_group, subject, classroom):
    """Фикстура периодического расписания"""
    from lesson_schedule import signals as lesson_signals
    from django.db.models.signals import post_save
    
    # Отключаем сигнал для контроля тестирования
    post_save.disconnect(lesson_signals.create_lessons_until_date, sender=PeriodSchedule)
    
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
    
    yield period_schedule
    
    # Восстанавливаем сигнал
    post_save.connect(lesson_signals.create_lessons_until_date, sender=PeriodSchedule)


@pytest.fixture
def valid_schedule_data(teacher, subject, classroom, student_group):
    """Фикстура валидных данных для создания занятия через API"""
    return {
        'title': 'Тестовое занятие',
        'date': '2024-01-15',
        'week_day': 1,
        'teacher': teacher.id,
        'group': student_group.id,
        'subject': subject.id,
        'classroom': classroom.id,
        'start_time': '09:00',
        'end_time': '10:30'
    }


# Новые фикстуры для тестирования
@pytest.fixture
def completed_schedule(organization, teacher, student_group, subject, classroom):
    """Фикстура завершенного занятия для тестов Celery"""
    return Schedule.objects.create(
        title="Завершенное занятие",
        date=date(2023, 12, 1),
        week_day=5,
        start_time=time(9, 0),
        end_time=time(10, 0),
        teacher=teacher,
        group=student_group,
        subject=subject,
        classroom=classroom,
        is_completed=True,
        org=organization
    )