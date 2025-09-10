from rest_framework import status
from mainapp.tests import BaseSetupDB

class TestChangeTeacherFields(BaseSetupDB):

    def test1(self):
        employer = self.employer2
        teacher = self.teacher1
        teacher_id = teacher.id
        url = f"/api/employers/teachers/{teacher_id}/"

        data = {'employer': employer.id}

        response = self.client.patch(url, data, format='json')

        self.assertIn(
            response.status_code,
            [status.HTTP_400_BAD_REQUEST,]
        )

        teacher.refresh_from_db()
        self.assertNotEqual(
            teacher.employer.id, 
            employer.id 
        )


