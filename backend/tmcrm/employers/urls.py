from email.mime import base
from django.urls import path
from mainapp.views import *
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TeacherViewset,
    EmployerViewSet,
    DownloadDocumentViewset,
    DepartmentViewSet,
    LeaveViewSet,
)

router = DefaultRouter()
router.register(r'employers', EmployerViewSet, basename='employer')
router.register(r'teachers', TeacherViewset, basename='teacher')
router.register(r'documents', DownloadDocumentViewset, basename='documents')
router.register(r"departments", DepartmentViewSet, basename="department")
router.register(r"leaves", LeaveViewSet, basename="leave")

urlpatterns = [
    path('', include(router.urls))
]
