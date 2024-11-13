from rest_framework.permissions import BasePermission, IsAuthenticated


class IsSuperUserOrReadOnly(BasePermission):

    # Custom permission to only allow superusers to create, update, and delete items.
    def has_permission(self, request, view):
        # Allow read-only requests for authenticated users
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        # Allow create, update, and delete for superusers only
        return (
            request.user and request.user.is_authenticated and request.user.is_superuser
        )
