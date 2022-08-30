from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Кастомное разрешение,
    только автор имеет право на редактирование."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class AdminOrReadOnly(permissions.BasePermission):
    """Permission to CRUD genres, category, titles in database"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin')


class SignupPermission(permissions.BasePermission):
    """
    Allow make request to 'signup' endpoint for admin and anonyms user.
    """

    def has_permission(self, request, view):
        return (not request.user.is_authenticated
                or request.user.role == 'admin')


class AdminPermission(permissions.BasePermission):
    """Allow make request for admin only."""

    def has_permission(self, request, view):
        return not request.user.is_anonymous and request.user.role == 'admin'


class IsSuperUserPermission(permissions.BasePermission):
    """Allow make request for superuser"""

    def has_permission(self, request, view):
        return request.user.is_superuser is True
