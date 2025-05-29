from django.shortcuts import render
from .permissions import IsSameOrganization
from rest_framework.viewsets import ViewSet, ModelViewSet



class BaseViewSetWithOrdByOrg(ModelViewSet):
    """
    Базовый ViewSet с автоматической фильтрацией по организации пользователя
    и дополнительными проверками прав доступа
    """
    permission_classes = [IsSameOrganization]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Если пользователь админ - показываем все записи
        if user.is_superuser or user.role == 'admin':
            return queryset
            
        # Для обычных пользователей - фильтр по организации
        if hasattr(user, 'org') and user.org:
            return queryset.filter(org=user.org)
            
        # Если у пользователя нет организации - пустой queryset
        return queryset.none()
    

