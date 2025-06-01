from django.urls import path
from mainapp.views import *
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduleViewSet

schedule_router = DefaultRouter()
schedule_router.register(r'', ScheduleViewSet, basename='schedule')


urlpatterns = schedule_router.urls
