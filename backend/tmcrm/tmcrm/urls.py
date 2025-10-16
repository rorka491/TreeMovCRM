from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.views.generic import RedirectView

from lesson_schedule.urls import router as schedule_router
from employers.urls import router as employers_router
from students.urls import router as students_router


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("tmcrm.api_urls")),
    path("", include("mainapp.urls")),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
