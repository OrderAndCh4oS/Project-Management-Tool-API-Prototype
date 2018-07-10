from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from project_management import permissions
from project_management import models
from project_management import serializers


class AddressViewSet(viewsets.ModelViewSet):
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)


class JobViewSet(viewsets.ModelViewSet):
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)


class StaffViewSet(viewsets.ModelViewSet):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)


class StatusGroupViewSet(viewsets.ModelViewSet):
    queryset = models.StatusGroup.objects.all()
    serializer_class = serializers.StatusGroupSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)


class CreateUserViewSet(mixins.CreateModelMixin, GenericViewSet):
    model = models.User
    permission_classes = [
        AllowAny  # Or anon users can't register
    ]
    serializer_class = serializers.CreateUserSerializer