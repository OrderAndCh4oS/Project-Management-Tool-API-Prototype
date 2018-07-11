from rest_framework import filters


class hasObjectAuthorityFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see objects in their authority
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(authority=request.session.get('authority'))
