from rest_framework import filters

from project_management.authority import get_the_authority


class hasObjectAuthorityFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(authority=get_the_authority(request.user))
