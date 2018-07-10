from rest_framework import permissions

from project_management.models import Staff


class IsAccountHolder(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_superuser:
            return True
        try:
            return request.user and request.user.is_account_holder and request.user == obj.account_holder
        except:
            return False


class IsProjectManager(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_superuser:
            return True
        try:
            staff = Staff.objects.get(user=request.user)
            return (
                    staff and staff.user.is_project_manager and
                    obj.account_holder == staff.account_holder
            )
        except:
            return False


class IsProjectManagerOrIsStaffReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_superuser:
            return True
        try:
            staff = Staff.objects.get(user=request.user)
            return (
                    (staff.user and staff.user.is_project_manager or
                     request.method in permissions.SAFE_METHODS and
                     staff.user and staff.user.is_authenticated)
                    and (obj.account_holder == staff.account_holder)
            )

        except:
            return False
