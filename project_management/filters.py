from rest_framework import filters


class hasObjectAuthorityFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(authority=request.session.get('authority'))
