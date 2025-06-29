from django.urls import path
from mainapp.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from django.views.generic import RedirectView





urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
]
