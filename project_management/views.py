from rest_framework import viewsets

from project_management import permissions
from project_management.models import Address, StatusGroup, Staff, Job, Project, Company, Client
from project_management.serializers import AddressSerializer, StatusGroupSerializer, StaffSerializer, JobSerializer, \
    ProjectSerializer, ClientSerializer, CompanySerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)


class StatusGroupViewSet(viewsets.ModelViewSet):
    queryset = StatusGroup.objects.all()
    serializer_class = StatusGroupSerializer
    permission_classes = (permissions.IsProjectManagerOrIsStaffReadOnly,)
