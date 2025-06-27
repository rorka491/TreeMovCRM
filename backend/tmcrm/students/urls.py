from django.urls import path, include
from mainapp.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .views import *
from rest_framework_nested import routers


router = routers.DefaultRouter()


router.register(r'', StudentViewSet, basename='student')
router.register(r'parents', ParentViewSet, basename='parent')
router.register(r'student_groups', StudentGroupViewSet, basename='student_group')

#вложенный роутер работает как
#students/1/grades/
#lookup='student' → URL-параметр будет student_pk
students_router = routers.NestedDefaultRouter(router, r'', lookup='student')
students_router.register('grades', StudentGradeViewSet, basename='student-grades')


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(students_router.urls)),
]

urlpatterns += router.urls 
urlpatterns += students_router.urls




