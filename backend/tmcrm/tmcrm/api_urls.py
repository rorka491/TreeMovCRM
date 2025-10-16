from django.urls import include, path 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from mainapp.urls import router as mainapp_router


urlpatterns = [
    path("auth/", include("accounts.urls")),
    path("students/", include("students.urls")),
    path("schedules/", include("lesson_schedule.urls")),
    path("employers/", include("employers.urls")),
    path("analisys/", include("analisys.urls")),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(mainapp_router.urls)),
]














