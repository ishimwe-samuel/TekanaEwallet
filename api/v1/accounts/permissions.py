from rest_framework.permissions import BasePermission


class IsAccountOwmer(BasePermission):
    message = "Only the account owner can perform this action"
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        return obj.user==request.user
