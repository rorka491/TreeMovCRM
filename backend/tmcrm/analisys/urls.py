from django.urls import path, include
from mainapp.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import MetricsViewSet, AnalyticsChartsViewSet

router = DefaultRouter()
router.register(r"metrics", MetricsViewSet, basename="metric")
router.register(r'charts', AnalyticsChartsViewSet, basename='chart')


urlpatterns = [path("", include(router.urls))]
