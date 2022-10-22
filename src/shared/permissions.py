from rest_framework.request import Request
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        return bool(request.user and request.user.is_admin)


class IsAuthor(BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        return bool(request.user and hasattr(request.user, 'author'))
