from rest_framework import permissions
from mainapp.models import BaseModelOrg

class IsSameOrganization(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: BaseModelOrg):
        # CHANGE IN PROD
        # return True
        if request.user.is_superuser == True:
            return True
        
        if hasattr(request.user, "org"):
            return obj.org == request.user.org
        
        return False
    





