<<<<<<< HEAD
from rest_framework.routers import DefaultRouter  
from .views import EmployerViewSet  


router = DefaultRouter()  
router.register(r'employers', EmployerViewSet, basename='employer')  

urlpatterns = router.urls  

# from django.urls import path
# from mainapp.views import *
# from django.conf import settings
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ScheduleViewSet
=======
from django.urls import path
from mainapp.views import *
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherViewset, EmployerViewSet
>>>>>>> main

employers_router = DefaultRouter()
employers_router.register(r'employers', EmployerViewSet, basename='employer')
employers_router.register(r'teachers', TeacherViewset, basename='teacher')

<<<<<<< HEAD
# urlpatterns = emploers_router.urls

=======
urlpatterns = [

]

urlpatterns += employers_router.urls
>>>>>>> main
