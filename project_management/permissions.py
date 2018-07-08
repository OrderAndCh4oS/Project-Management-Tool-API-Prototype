from rest_framework import permissions


class IsProjectManager(permissions.BasePermission):
    """
    Allows access only to project managers users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_project_manager or request.user and request.user.is_superuser


class IsProjectManagerOrIsStaffReadOnly(permissions.BasePermission):
    """
    Allows access only to project managers users or read only access to staff members.
    """

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS and
                request.user and request.user.is_staff_member or
                request.user and request.user.is_project_manager or
                request.user and request.user.is_superuser
        )
