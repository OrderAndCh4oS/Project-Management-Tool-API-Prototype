from rest_framework import viewsets

from project_management.models import Address, StatusGroup, Staff, Job, Project, Company, Client
from project_management.serializers import AddressSerializer, StatusGroupSerializer, StaffSerializer, JobSerializer, \
    ProjectSerializer, ClientSerializer, CompanySerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class StatusGroupViewSet(viewsets.ModelViewSet):
    queryset = StatusGroup.objects.all()
    serializer_class = StatusGroupSerializer
