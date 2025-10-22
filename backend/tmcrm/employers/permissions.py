from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied



class IsTeacherProfile(permissions.BasePermission): 
    
    def has_permission(self, request, view):
        teacher_profile = request.user.get_teacher_profile()
        if not teacher_profile: 
            raise PermissionDenied("Вы не учитель операция не доступна")

        return True
