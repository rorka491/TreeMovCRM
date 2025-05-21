from django.urls import path
from mainapp.views import *
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import *


schedule_router = DefaultRouter()
schedule_router.register(r'', ScheduleViewSet, basename='schedule')
schedule_router.register(r'', ScheduleByTeacherViewSet, basename='schedule/by_teachers')


urlpatterns = schedule_router.urls





