from rest_framework import permissions

class IsOwnerSharedOrPublic(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.access_level == "public":
            return True
        if obj.access_level == "private":
            return obj.owner == request.user
        if obj.access_level == "shared":
            return obj.owner == request.user or request.user in obj.shared_with.all()
        return False
    
                                             