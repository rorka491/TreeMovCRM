from rest_framework import permissions
from mainapp.models import BaseModelOrg

class IsSameOrganization(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: BaseModelOrg):
        return True
        if request.user.is_superuser == True:
            return True
        
        return obj.org == request.user.org
    





