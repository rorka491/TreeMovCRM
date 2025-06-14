from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from schedule.urls import schedule_router
from employers.urls import employers_router
from students.urls import students_router




urlpatterns = [
    path('schedules/', include(schedule_router.urls)),
    path('employers/', include(employers_router.urls)),
    path('students/', include(students_router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
