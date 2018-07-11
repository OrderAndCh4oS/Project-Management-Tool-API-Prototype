from rest_framework import permissions

from project_management.authority import has_access


class IsProjectManager(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        try:
            return request.user and request.user.is_project_manager
        except:
            return False

    def has_object_permission(self, request, view, obj):
        return has_access(request, obj) and request.user.is_project_manager


class IsProjectManagerOrIsStaffReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        try:
            return (
                    request.user and request.user.is_project_manager or
                    request.method in permissions.SAFE_METHODS and
                    request.user and request.user.is_authenticated
            )
        except:
            return False

    def has_object_permission(self, request, view, obj):
        return (
                has_access(request, obj) and request.user.is_project_manager or
                has_access(request, obj) and request.method in permissions.SAFE_METHODS
        )
