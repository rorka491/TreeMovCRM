from typing import TYPE_CHECKING
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import RegeisterConfirmSerializer, RegisterStartSerializer
from .utils import generate_six_digit_code
from .models import Invite
from django.contrib.auth import get_user_model


if TYPE_CHECKING: 
    from rest_framework.request import Request

class RegisterStartView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request) -> Response:
        serializer = RegisterStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data
    
        email = validated["email"]
        username = validated["username"]
        password = validated["password"]

        code = generate_six_digit_code()

        cache.set(
            f"reg_2fa:{email}",
            {
                "username": username,
                "password": password,
                "code": code,
            },
            timeout=300,
        )

        return Response({"detail": "Code sent"})



class RegisterConfirmView(APIView):


    def post(self, request) -> Response:
        serializer = RegeisterConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        email = validated["email"]
        code = validated["code"]

        cache_user_data = cache.get(f"reg_2fa:{email}", None)
        if not cache_user_data:
            return Response(
                {"code": 404, "detail": "Registration data not found or expired."}
            )

        if code == cache_user_data["code"]:
            username = cache_user_data["username"]
            password = cache_user_data["password"]
            User = get_user_model()
            User.objects.create_user(username=username, password=password)
            return Response(
                {"code": 200, "detail": f"User {username} created successfully."}
            )
        return Response({"code": 403, "detail": "Invalid confirmation code."})


class CreateInviteLink(APIView): 


    def post(self, request): 
        org = request.user.get_org
        invite = Invite.create_manager.create()
        link = request.build_absolute_uri(f"/join/{invite.token}/")
        return Response({"invite_link": link})

class JoinOrganizationView(APIView):

    def post(self, request, token) -> Response:
        ...
