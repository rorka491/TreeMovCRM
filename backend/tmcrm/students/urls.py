from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from .views import (
    StudentViewSet,
    ParentViewSet,
    StudentGroupViewSet,
    StudentGradeViewSet,
    AccrualViewSet,
)


router = routers.DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'parents', ParentViewSet, basename='parent')
router.register(r'student_groups', StudentGroupViewSet, basename='student_group')
router.register(r'grades', StudentGradeViewSet, basename='all-student-grades') 
router.register(r"accruals", AccrualViewSet, basename="accruals")


# вложенный роутер работает как
# students/1/grades/
# lookup='student' → URL-параметр будет student_pk
students_router = nested_routers.NestedDefaultRouter(
    router, r"students", lookup="student"
)
students_router.register(r'grades', StudentGradeViewSet, basename='student-grades')


student_groups_router = nested_routers.NestedDefaultRouter(
    router, r"student_groups", lookup="student_group"
)
student_groups_router.register(r'students', StudentViewSet)


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(students_router.urls)),
]
