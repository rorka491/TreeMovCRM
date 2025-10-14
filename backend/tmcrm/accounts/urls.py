from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterStartView, RegisterConfirmView, JoinOrganizationView, CreateInviteLink


urlpatterns = [
    path("sign_up/", RegisterStartView.as_view()),
    path("confirm_sign_up/", RegisterConfirmView.as_view()),
    path("join/<uuid:token>", JoinOrganizationView.as_view()),
    path("create_invite", CreateInviteLink.as_view()),
]
