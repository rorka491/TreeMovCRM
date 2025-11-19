from django.urls import path
from mainapp.views import *
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"lessons", ScheduleViewSet, basename="lesson")
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'classrooms', ClassroomViewSet, basename='classroom')
router.register(r'attendances', AttendanceViewSet, basename='attendance')
router.register(r'period_lessons', PeriodScheduleViewSet, basename='period_lesson')
router.register(r'subject_colors', SubjectColorViewSet, basename="subject_color")
router.register(r'grades', GradeViewSet, basename='grade')


urlpatterns = [
    path('', include(router.urls))
]