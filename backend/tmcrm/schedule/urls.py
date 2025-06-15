from django.urls import path
from mainapp.views import *
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

schedule_router = DefaultRouter()
schedule_router.register(r'schedules', ScheduleViewSet, basename='schedule')
schedule_router.register(r'subjects', SubjectViewSet, basename='subject')
schedule_router.register(r'classrooms', ClassroomViewSet, basename='classroom')
schedule_router.register(r'grades', GradeViewSet, basename='grade')
schedule_router.register(r'attendances', AttendanceViewSet, basename='attendance')

urlpatterns = schedule_router.urls
