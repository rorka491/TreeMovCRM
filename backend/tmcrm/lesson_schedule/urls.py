from django.urls import path
from mainapp.views import *
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'schedules', ScheduleViewSet, basename='schedule')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'classrooms', ClassroomViewSet, basename='classroom')
router.register(r'attendances', AttendanceViewSet, basename='attendance')
router.register(r'period_schedules', PeriodScheduleViewSet, basename='period_schedule')



urlpatterns = [
    path('', include(router.urls))
]


