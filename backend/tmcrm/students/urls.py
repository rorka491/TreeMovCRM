from django.urls import path  
from rest_framework.routers import DefaultRouter  
from .views import *


student_router = DefaultRouter()  
student_router.register(r'', StudentViewSet, basename='students') 
student_router.register(r'students_group', StudentGroupViewSet, basename='students_group')


urlpatterns = student_router.urls