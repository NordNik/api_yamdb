from rest_framework import permissions


class SignupPermission(permissions.BasePermission):
    """
    Allow make request to 'signup' endpoint for admin and anonyms user.
    """

    def has_permission(self, request, view):
        return (
            not request.user.is_authenticated or request.user.role == 'admin'
        )


class AdminPermission(permissions.BasePermission):
    """Allow make request for admin only."""

    def has_permission(self, request, view):
        return not request.user.is_anonymous and request.user.role == 'admin'


class IsSuperUserPermission(permissions.BasePermission):
    """Allow make request for superuser"""

    def has_permission(self, request, view):
        return request.user.is_superuser is True
