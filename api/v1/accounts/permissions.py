from rest_framework.permissions import BasePermission


class IsAccountOwmer(BasePermission):
    message = "Only the account owner can perform this action"
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            if not request.user.has_account:
                self.message = "User does not have an account"
                return False
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return obj.user==request.user
