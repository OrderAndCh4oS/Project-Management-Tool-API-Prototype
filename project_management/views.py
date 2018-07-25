from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from project_management import models
from project_management import permissions
from project_management import serializers
from project_management.authority import get_the_authority
from project_management.filters import hasObjectAuthorityFilterBackend
from project_management.models import Authority


class WithAuthorityBaseViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        authority = Authority.objects.get(uuid=get_the_authority(self.request.user))
        serializer.save(authority=authority)


class AddressViewSet(WithAuthorityBaseViewSet):
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)
    filter_backends = (hasObjectAuthorityFilterBackend,)


class CompanyViewSet(WithAuthorityBaseViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, hasObjectAuthorityFilterBackend)
    search_fields = ('name', 'clients__fullname')
    filter_fields = ('clients__fullname',)


class ClientViewSet(WithAuthorityBaseViewSet):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, hasObjectAuthorityFilterBackend)
    search_fields = ('fullname', 'companies__name', 'email_addresses__email')
    filter_fields = ('companies__name',)


class EmailAddressViewSet(WithAuthorityBaseViewSet):
    queryset = models.EmailAddress.objects.all()
    serializer_class = serializers.EmailAddressSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)
    filter_backends = (hasObjectAuthorityFilterBackend,)


class ProjectViewSet(WithAuthorityBaseViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, hasObjectAuthorityFilterBackend)
    search_fields = ('reference_code', 'company__name')
    filter_fields = ('company__name',)


class JobViewSet(WithAuthorityBaseViewSet):
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, hasObjectAuthorityFilterBackend)
    search_fields = ('todo__reference_code', 'todo__title', 'todo__description')
    filter_fields = (
        'todo__assigned_to__user__username',
        'todo__assigned_to__user__first_name', 'todo__assigned_to__user__last_name',
        'todo__status__title'
    )


class TaskViewSet(WithAuthorityBaseViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, hasObjectAuthorityFilterBackend)
    # search_fields = (
    #     'todo__reference_code', 'todo__title', 'todo__description',
    #     'job__todo__reference_code', 'job__todo__title', 'job__todo__description'
    # )
    # filter_fields = (
    #     'todo__project__reference_code', 'todo__assigned_to__user__username',
    #     'todo__assigned_to__user__first_name', 'todo__assigned_to__user__last_name',
    #     'todo__status__title'
    # )


class StaffViewSet(WithAuthorityBaseViewSet):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)
    filter_backends = (filters.SearchFilter, hasObjectAuthorityFilterBackend)
    search_fields = ('user',)


class StatusGroupViewSet(WithAuthorityBaseViewSet):
    queryset = models.StatusGroup.objects.all()
    serializer_class = serializers.StatusGroupSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)
    filter_backends = (hasObjectAuthorityFilterBackend,)


# Todo: filter by times gte lte
class WorkDayViewSet(WithAuthorityBaseViewSet):
    queryset = models.WorkDay.objects.all()
    serializer_class = serializers.WorkDaySerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)
    filter_backends = (hasObjectAuthorityFilterBackend,)


# Todo: filter by times gte lte
class ScheduledTodoViewSet(WithAuthorityBaseViewSet):
    queryset = models.ScheduledTodo.objects.all()
    serializer_class = serializers.ScheduledTodoSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)
    filter_backends = (hasObjectAuthorityFilterBackend,)
    filter_fields = (
        'work_day',
        'todo__project__reference_code', 'todo__assigned_to__user__username',
        'todo__assigned_to__user__first_name', 'todo__assigned_to__user__last_name',
        'todo__status__title'
    )


class StatusViewSet(WithAuthorityBaseViewSet):
    queryset = models.Status.objects.all()
    serializer_class = serializers.StatusSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)
    filter_backends = (hasObjectAuthorityFilterBackend,)


class CreateUserViewSet(mixins.CreateModelMixin, GenericViewSet):
    model = models.User
    permission_classes = (AllowAny,)
    serializer_class = serializers.CreateUserSerializer
