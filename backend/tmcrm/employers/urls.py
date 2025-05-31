<<<<<<< HEAD
from rest_framework.routers import DefaultRouter  
from .views import EmployerViewSet  

router = DefaultRouter()  
router.register(r'employers', EmployerViewSet, basename='employer')  

urlpatterns = router.urls  
=======
# from django.urls import path
# from mainapp.views import *
# from django.conf import settings
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ScheduleViewSet

# emploers_router = DefaultRouter()
# emploers_router.register(r'schedules', ScheduleViewSet, basename='schedule')

# urlpatterns = emploers_router.urls
>>>>>>> main
