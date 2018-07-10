from rest_framework import permissions


class IsAccountHolder(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        try:
            return request.user and request.user.is_account_holder
        except:
            return False


class IsProjectManager(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        try:
            return request.user and request.user.is_project_manager
        except:
            return False


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
