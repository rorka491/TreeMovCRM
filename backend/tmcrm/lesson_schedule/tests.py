from datetime import date, time
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from mainapp.tests import BaseSetupDB
from students.models import Student, StudentGroup
from lesson_schedule.models import Schedule, Classroom, Subject
from .serializers.read import ScheduleReadSerializer



class TestChangeCriticalScheduleFields(BaseSetupDB):

    def test_change_teacher(self):
        new_teacher = self.teacher1
        schedule = self.schedule2

        url = f"/api/schedules/schedules/{schedule.id}/"
        data = {"teacher": new_teacher.id}



        response = self.client.patch(url, data, format="json")

        # Ожидаем отказ, например 400 или 403
        self.assertIn(
            response.status_code,
            [status.HTTP_400_BAD_REQUEST, status.HTTP_403_FORBIDDEN],
        )

        schedule.refresh_from_db()
        self.assertNotEqual(schedule.teacher.id, new_teacher.id)

    def test_change_classroom(self):
        new_classrom = self.classroom1
        schedule = self.schedule2

        url = f"/api/schedules/schedules/{schedule.id}/"
        data = {"classroom": new_classrom.id}



        response = self.client.patch(url, data, format="json")

        self.assertIn(
            response.status_code,
            [status.HTTP_400_BAD_REQUEST, status.HTTP_403_FORBIDDEN],
        )

        schedule.refresh_from_db()
        self.assertNotEqual(schedule.classroom.id, new_classrom.id)

    def test_change_group(self):
        new_group = self.group1
        schedule = self.schedule2

        url = f"/api/schedules/schedules/{schedule.id}/"
        data = {"group": new_group.id}

        # access_token = self._get_access_token()
        # self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        response = self.client.patch(url, data, format="json")

        self.assertIn(
            response.status_code,
            [status.HTTP_400_BAD_REQUEST, status.HTTP_403_FORBIDDEN],
        )

        schedule.refresh_from_db()
        self.assertNotEqual(schedule.group.id, new_group.id)


class TestMoveTimeOuts(BaseSetupDB):

    def test1(self):
        schedule1 = self.schedule1
        new_end_time = "14:00:00"
        url = f"/api/schedules/schedules/{schedule1.id}/"
        data = {"end_time": new_end_time}

        response = self.client.patch(url, data, format="json")

        self.assertIn(
            response.status_code,
            [status.HTTP_400_BAD_REQUEST, status.HTTP_403_FORBIDDEN],
        )

        schedule1.refresh_from_db()
        new_end_time = time.fromisoformat(new_end_time)
        self.assertNotEqual(schedule1.end_time, new_end_time)

    def test2(self):
        schedule1 = self.schedule1
        new_end_time = "13:45:00"
        url = f"/api/schedules/schedules/{schedule1.id}/"
        data = {"end_time": new_end_time}



        response = self.client.patch(url, data, format="json")

        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK],
        )

        schedule1.refresh_from_db()
        new_end_time = time.fromisoformat(new_end_time)
        self.assertEqual(schedule1.end_time, new_end_time)


class TestInsertSchedule(BaseSetupDB):
    def test1(self):
        start_count = Schedule.objects.count()
        schedule1 = self.schedule1

        serializer = ScheduleReadSerializer(schedule1)
        data = serializer.data
        data.pop("id", None)
        url = f"/api/schedules/schedules/"

        response = self.client.post(url, data, format="json")
        self.assertIn(
            response.status_code,
            [status.HTTP_400_BAD_REQUEST, status.HTTP_403_FORBIDDEN],
        )

        end_count = Schedule.objects.count()
        schedule1.refresh_from_db()
        self.assertEqual(end_count, start_count)


class TestDeleteSchedule(BaseSetupDB):
    def test1(self):

        schedule1_id = self.schedule1.id
        Schedule.objects.get(pk=schedule1_id).delete()
