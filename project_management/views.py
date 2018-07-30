from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from project_management import models
from project_management import permissions
from project_management import serializers
from project_management.authority import get_the_authority
from project_management.filters import hasObjectAuthorityFilterBackend
from project_management.models import Authority


class WithAuthorityBaseViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)

    def perform_create(self, serializer):
        authority = Authority.objects.get(uuid=get_the_authority(self.request.user))
        serializer.save(authority=authority)


class AddressViewSet(WithAuthorityBaseViewSet):
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressSerializer
    filter_backends = (hasObjectAuthorityFilterBackend,)


class CompanyViewSet(WithAuthorityBaseViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, hasObjectAuthorityFilterBackend)
    search_fields = ('name', 'clients__fullname')
    filter_fields = ('clients__fullname',)


class ClientViewSet(WithAuthorityBaseViewSet):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, hasObjectAuthorityFilterBackend)
    search_fields = ('fullname', 'companies__name', 'email_addresses__email')
    filter_fields = ('companies__name',)


class EmailAddressViewSet(WithAuthorityBaseViewSet):
    queryset = models.EmailAddress.objects.all()
    serializer_class = serializers.EmailAddressSerializer
    filter_backends = (hasObjectAuthorityFilterBackend,)


class ProjectViewSet(WithAuthorityBaseViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, hasObjectAuthorityFilterBackend)
    search_fields = ('reference_code', 'company__name')
    filter_fields = ('company__name',)


class JobViewSet(WithAuthorityBaseViewSet):
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, hasObjectAuthorityFilterBackend)
    search_fields = ('todo__reference_code', 'todo__title', 'todo__description')
    filter_fields = (
        'todo__assigned_to__user__username',
        'todo__assigned_to__user__first_name', 'todo__assigned_to__user__last_name',
        'todo__status__title'
    )

    def get_queryset(self):
        username = self.request.query_params.get('todo__assigned_to__user__username', None)
        first_name = self.request.query_params.get('todo__assigned_to__user__first_name', None)
        last_name = self.request.query_params.get('todo__assigned_to__user__last_name', None)
        if not (username or first_name or last_name):
            user = self.request.user
            return models.Job.objects.filter(todo__assigned_to__user=user)
        return models.Job.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance.todo)
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)



class TaskViewSet(WithAuthorityBaseViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, hasObjectAuthorityFilterBackend)
    search_fields = ('todo__reference_code', 'todo__title', 'todo__description')
    filter_fields = (
        'todo__assigned_to__user__username',
        'todo__assigned_to__user__first_name', 'todo__assigned_to__user__last_name',
        'todo__status__title'
    )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance.todo)
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


class StaffViewSet(WithAuthorityBaseViewSet):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer
    filter_backends = (filters.SearchFilter, hasObjectAuthorityFilterBackend)
    search_fields = ('user',)


class StatusGroupViewSet(WithAuthorityBaseViewSet):
    queryset = models.StatusGroup.objects.all()
    serializer_class = serializers.StatusGroupSerializer
    filter_backends = (hasObjectAuthorityFilterBackend,)


# Todo: filter by times gte lte
class WorkDayViewSet(WithAuthorityBaseViewSet):
    queryset = models.WorkDay.objects.all()
    serializer_class = serializers.WorkDaySerializer
    filter_backends = (hasObjectAuthorityFilterBackend,)


# Todo: filter by times gte lte
class ScheduledTodoViewSet(WithAuthorityBaseViewSet):
    queryset = models.ScheduledTodo.objects.all()
    serializer_class = serializers.ScheduledTodoSerializer
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
    filter_backends = (hasObjectAuthorityFilterBackend,)


class CreateUserViewSet(mixins.CreateModelMixin, GenericViewSet):
    model = models.User
    permission_classes = (AllowAny,)
    serializer_class = serializers.CreateUserSerializer
