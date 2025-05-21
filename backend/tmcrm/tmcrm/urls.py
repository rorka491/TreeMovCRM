from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomApiRoot  


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
    path('api/', CustomApiRoot.as_view()),
    path('api/analysis/', include('analisys.urls')),
    path('api/financial_reporting/', include('financial_reporting.urls')),
    path('api/students/', include('students.urls')),
    path('api/schedules/', include('schedule.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





