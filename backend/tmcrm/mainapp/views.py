import traceback
from django.shortcuts import render
from .permissions import IsSameOrganization
from rest_framework.viewsets import ViewSet, ModelViewSet
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView


class BaseViewAuthPermission(ModelViewSet):

    permission_classes = [IsAuthenticated]


class BaseViewSetWithOrdByOrg(BaseViewAuthPermission):
    """
    Базовый ViewSet с автоматической фильтрацией по организации пользователя
    и дополнительными проверками прав доступа
    """
    permission_classes += [IsSameOrganization, IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Если пользователь админ - показываем все записи
        if user.is_superuser or user.role == 'admin':
            return queryset
            
        # Для обычных пользователей - фильтр по организации
        if hasattr(user, 'org') and user.org:
            return queryset.filter(org=user.org)

        if hasattr(user, 'org') and user.org:
            return queryset  

        return queryset
    

class SelectRelatedViewSet(ModelViewSet):
    """
    Класс который будет использоваться для оптимизированных запросов 
    и решения N+1 проблемы
    Наследовать после BaseViewSetWithOrdByOrg если есть 
    наседование от этого класса
    """

    select_related_fields = []
    prefetch_related_fields = []

    def get_queryset(self):
        qs = super().get_queryset()

        if self.select_related_fields:
            qs = qs.select_related(*self.select_related_fields)
        if self.prefetch_related_fields:
            qs = qs.prefetch_related(*self.prefetch_related_fields)

        return qs 
    

    
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'detail': 'Успешный вход'})
        return Response({'detail': 'Неверные данные'}, status=400)



@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': 'Выход выполнен'})

