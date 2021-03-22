from rest_framework import permissions


class IsAdminOnly(permissions.BasePermission):
    """
    Allows access only to admin or django_admin users.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin
        return False
