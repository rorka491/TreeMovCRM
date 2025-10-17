from django.test import TestCase
from django.urls import reverse, resolve
from employers.views import TeacherViewset, EmployerViewSet, DownloadDocumentViewset

class EmployersUrlsTest(TestCase):

    def test_employers_list_url(self):
        """Тест URL для списка сотрудников"""
        url = reverse('employer-list')
        self.assertEqual(resolve(url).func.cls, EmployerViewSet)

    def test_employers_detail_url(self):
        """Тест URL для деталей сотрудника"""
        url = reverse('employer-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, EmployerViewSet)

    def test_teachers_list_url(self):
        """Тест URL для списка преподавателей"""
        url = reverse('teacher-list')
        self.assertEqual(resolve(url).func.cls, TeacherViewset)

    def test_teachers_detail_url(self):
        """Тест URL для деталей преподавателя"""
        url = reverse('teacher-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, TeacherViewset)

    def test_documents_list_url(self):
        """Тест URL для списка документов"""
        url = reverse('documents-list')
        self.assertEqual(resolve(url).func.cls, DownloadDocumentViewset)

    def test_documents_detail_url(self):
        """Тест URL для деталей документа"""
        url = reverse('documents-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, DownloadDocumentViewset)

    def test_documents_response_url_resolved(self):
        """Тест что URL для response_documents корректно настроен"""
        # Проверяем что action зарегистрирован
        viewset = DownloadDocumentViewset()
        actions = viewset.get_extra_actions()
        response_action = [action for action in actions if action.url_path == 'response_documents']
        self.assertEqual(len(response_action), 1)