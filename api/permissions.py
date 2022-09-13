from rest_framework.permissions import BasePermission


class IsRequesterAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)
