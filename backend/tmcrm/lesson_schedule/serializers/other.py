from rest_framework import serializers
from employers.serializers.read import TeacherReadSerializer
from students.serializers.read import StudentGroupReadSerializer
from .read import ClassroomReadSerializer, ScheduleReadSerializer


class ScheduleStudentGroupSerializer(serializers.Serializer):
    schedules = serializers.SerializerMethodField()
    exclude_fields = []

    def get_schedules(self, obj):
        schedules_qs = obj["schedules"]
        return ScheduleReadSerializer(
            schedules_qs, many=True, exclude_fields=self.exclude_fields
        ).data


class TeacherScheduleSerializer(ScheduleStudentGroupSerializer):
    """"""

    teacher = TeacherReadSerializer()
    exclude_fields = ["teacher"]

    class Meta:
        fields = ["teacher", "schedules"]


class ClassroomScheduleSerializer(ScheduleStudentGroupSerializer):
    """"""

    classroom = ClassroomReadSerializer()
    exclude_fields = ["classroom"]

    class Meta:
        fields = ["classroom", "schedules"]


class GroupScheduleSerializer(ScheduleStudentGroupSerializer):
    """"""

    group = StudentGroupReadSerializer(exclude_fields=["students"])
    exclude_fields = ["group"]

    class Meta:
        fields = ["group", "schedules"]
