from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAdmibOrReadOnly(permissions.BasePermission):  # type: ignore[misc]
    """Allow only admins to modify objects, others can read."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method == permissions.SAFE_METHODS:
            return True
        return bool(
            request.user 
            and request.user.is_authenticated
            and request.user.is_admin
        )
