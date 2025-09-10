from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterStartView, RegisterConfirmView


urlpatterns = [
    path("sign_up/", RegisterStartView.as_view()),
    path("confirm_sign_up/", RegisterConfirmView.as_view()),
]
