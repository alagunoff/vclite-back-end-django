from rest_framework.exceptions import NotFound
from rest_framework.permissions import BasePermission


class IsRequesterAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated or not request.user.is_admin:
            raise NotFound()

        return True
