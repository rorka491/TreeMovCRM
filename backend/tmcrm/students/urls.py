from django.urls import path
from mainapp.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import *


students_router = DefaultRouter()
students_router.register(r'student_groups', StudentGroupViewSet, basename='student_group')


urlpatterns = [

]

urlpatterns += students_router.urls
