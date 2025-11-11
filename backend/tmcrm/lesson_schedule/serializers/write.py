from rest_framework import serializers
from employers.models import Teacher
from students.models import Student, StudentGroup
from lesson_schedule.models import (
    Attendance,
    Classroom,
    Schedule,
    Subject,
    PeriodSchedule,
    Grade,
)
from mainapp.models import SubjectColor
from mainapp.serializers import BaseWriteSerializer, ColorSerializer


class ClassroomWriteSerializer(BaseWriteSerializer):

    class Meta(BaseWriteSerializer.Meta):
        model = Classroom


class SubjectWriteSerializer(BaseWriteSerializer):
    color = serializers.PrimaryKeyRelatedField(queryset=SubjectColor.objects.all())

    class Meta(BaseWriteSerializer.Meta):
        model = Subject


class AttendanceWriteSerializer(BaseWriteSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    lesson = serializers.PrimaryKeyRelatedField(queryset=Schedule.objects.all())

    class Meta(BaseWriteSerializer.Meta):
        model = Attendance


class ScheduleWriteSerializer(BaseWriteSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=StudentGroup.objects.all())
    classroom = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())

    class Meta(BaseWriteSerializer.Meta):
        model = Schedule

    def validate(self, data):
        """Дополнительная валидация для предотвращения конфликтов расписания"""
        instance = self.instance
        date = data.get('date', getattr(instance, 'date', None))
        start_time = data.get('start_time', getattr(instance, 'start_time', None))
        end_time = data.get('end_time', getattr(instance, 'end_time', None))
        teacher = data.get('teacher', getattr(instance, 'teacher', None))
        group = data.get('group', getattr(instance, 'group', None))

        # Проверяем конфликты только если есть все необходимые данные
        if date and start_time and end_time:
            # Проверяем конфликты преподавателя
            if teacher:
                teacher_conflicts = Schedule.objects.filter(
                    date=date,
                    teacher=teacher,
                    start_time=start_time,
                    end_time=end_time
                )
                if instance:
                    teacher_conflicts = teacher_conflicts.exclude(pk=instance.pk)
                if teacher_conflicts.exists():
                    raise serializers.ValidationError({
                        'teacher': 'Этот преподаватель уже занят в это время'
                    })

            # Проверяем конфликты группы
            if group:
                group_conflicts = Schedule.objects.filter(
                    date=date,
                    group=group,
                    start_time=start_time,
                    end_time=end_time
                )
                if instance:
                    group_conflicts = group_conflicts.exclude(pk=instance.pk)
                if group_conflicts.exists():
                    raise serializers.ValidationError({
                        'group': 'Эта группа уже занята в это время'
                    })

        return data


class PeriodScheduleWriteSerializer(BaseWriteSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=StudentGroup.objects.all())
    classroom = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())

    class Meta(BaseWriteSerializer.Meta):
        model = PeriodSchedule


class GradeWriteSerializer(BaseWriteSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    lesson = serializers.PrimaryKeyRelatedField(queryset=Schedule.objects.all())

    class Meta(BaseWriteSerializer.Meta):
        model = Grade