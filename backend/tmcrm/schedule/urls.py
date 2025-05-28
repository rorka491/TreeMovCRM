from django.urls import path
from mainapp.views import *
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import *


schedule_router = DefaultRouter()
schedule_router.register(r'', ScheduleViewSet, basename='schedules') 
schedule_router.register(r'subjects', SubjectViewSet, basename='subjects')  
schedule_router.register(r'attendances', AttendanceViewSet, basename='attendances')  
schedule_router.register(r'grades', GradeViewSet, basename='grades') 


urlpatterns = schedule_router.urls





