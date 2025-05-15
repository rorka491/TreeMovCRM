from django.urls import path
from mainapp.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView



urlpatterns = [
    path('', TemplateView.as_view(template_name='pages/test_page.html'))
]