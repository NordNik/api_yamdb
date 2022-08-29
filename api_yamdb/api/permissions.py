from rest_framework.permissions import SAFE_METHODS, BasePermission


class StaffOrAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in SAFE_METHODS
                or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.role == 'admin'
            or request.user.role == 'moderator'

        )
