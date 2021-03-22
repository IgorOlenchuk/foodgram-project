from rest_framework import permissions
from users.models import User


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin
        return request.method in permissions.SAFE_METHODS
        

class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'POST':
            return request.user.is_authenticated

        return request.user.is_authenticated and (
                    request.user == obj.author or
                    request.user.is_admin or
                    request.user.role == 'moderator'
            )


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_admin or
                request.user.is_staff
            )
        )