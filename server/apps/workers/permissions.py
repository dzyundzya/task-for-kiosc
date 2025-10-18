from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAdmibOrReadOnly(permissions.BasePermission):  # type: ignore[misc]
    """Allow only admins to modify objects, others can read."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Grant access if request is safe or user is an admin."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated and request.user.is_admin)
