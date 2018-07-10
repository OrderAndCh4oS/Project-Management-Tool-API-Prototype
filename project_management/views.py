from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from project_management import models
from project_management import permissions
from project_management import serializers
from project_management.models import Staff


class BaseModelViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        if self.request.user.is_account_holder:
            serializer.save(account_holder=self.request.user)
        else:
            staff = Staff.objects.filter(user=self.request.user)
            serializer.save(account_holder=staff.account_holder)


class AddressViewSet(BaseModelViewSet):
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)


class CompanyViewSet(BaseModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('name', 'clients__fullname')
    filter_fields = ('clients__fullname',)

    def perform_create(self, serializer):
        self.assign_account_holder(serializer)


class ClientViewSet(BaseModelViewSet):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('fullname', 'companies__name', 'email_addresses__email')
    filter_fields = ('companies__name',)


class EmailAddressViewSet(BaseModelViewSet):
    queryset = models.EmailAddress.objects.all()
    serializer_class = serializers.EmailAddressSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)


class ProjectViewSet(BaseModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('reference_code', 'company__name')
    filter_fields = ('company__name',)


class JobViewSet(BaseModelViewSet):
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('reference_code', 'title', 'description')
    filter_fields = (
        'project__reference_code', 'assigned_to__username',
        'assigned_to__first_name', 'assigned_to__last_name',
        'status__title'
    )


class StaffViewSet(BaseModelViewSet):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user',)


class StatusGroupViewSet(BaseModelViewSet):
    queryset = models.StatusGroup.objects.all()
    serializer_class = serializers.StatusGroupSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)


class CreateUserViewSet(mixins.CreateModelMixin, GenericViewSet):
    model = models.User
    permission_classes = (AllowAny,)
    serializer_class = serializers.CreateUserSerializer
