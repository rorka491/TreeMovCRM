from typing import TYPE_CHECKING
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import RegeisterConfirmSerializer, RegisterStartSerializer
from .utils import generate_six_digit_code, send_email
from .models import Invite
from django.contrib.auth import get_user_model
from mainapp.permissions import IsSameOrganization

                                
if TYPE_CHECKING: 
    from rest_framework.request import Request
                        
class RegisterStartView(APIView):

    def post(self, request) -> Response:
        serializer = RegisterStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        email = validated["email"]
        username = validated["username"]
        password = validated["password"]

        code = generate_six_digit_code()
        
        email_sent = send_email(email, code)
        
        if not email_sent:
            return Response(
                {"detail": "Не удалось отправить код подтверждения на email"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        cache.set(
            f"reg_2fa:{email}",
            {
                "username": username,
                "password": password,
                "code": code,
            },
            timeout=300,
        )

        return Response({"detail": "Код подтверждения отправлен на вашу почту"})


class RegisterConfirmView(APIView):
    permission_classes = [IsAuthenticated, IsSameOrganization]

    def post(self, request) -> Response:
        serializer = RegeisterConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        email = validated["email"]
        code = validated["code"]

        cache_user_data = cache.get(f"reg_2fa:{email}", None)
        if not cache_user_data:
            return Response(
                {"code": 404, "detail": "Данные регистрации не найдены или истекли."}
            )

        if code == cache_user_data["code"]:
            username = cache_user_data["username"]
            password = cache_user_data["password"]
            User = get_user_model()
            User.objects.create_user(username=username, password=password)
            
            cache.delete(f"reg_2fa:{email}")
            
            return Response(
                {"code": 200, "detail": f"Пользователь {username} успешно создан."}
            )
        return Response({"code": 403, "detail": "Неверный код подтверждения."})


class CreateInviteLink(APIView): 
    permission_classes = [IsAuthenticated, IsSameOrganization]

    def post(self, request): 
        org = request.user.get_org
        invite = Invite.create_manager.create()
        link = request.build_absolute_uri(f"/join/{invite.token}/")
        return Response({"invite_link": link})

class JoinOrganizationView(APIView):

    def post(self, request, token) -> Response:
        ...