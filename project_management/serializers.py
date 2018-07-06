from rest_framework import serializers

from project_management.models import Address, Company, Client, StatusGroup, Staff, Job, Project, EmailAddress, Status


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    clients = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='client-detail',
        queryset=Client.objects.all()
    )
    addresses = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='address-detail',
        queryset=Address.objects.all()
    )

    class Meta:
        model = Company
        fields = ('name', 'url', 'clients', 'addresses')


class ClientSerializer(serializers.ModelSerializer):
    email_address = serializers.SlugRelatedField(slug_field='email', queryset=EmailAddress.objects.all())
    class Meta:
        model = Client
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    company = serializers.HyperlinkedRelatedField(
        view_name='company-detail',
        queryset=Company.objects.all()
    )
    class Meta:
        model = Project
        exclude = ('status_group',)


class JobSerializer(serializers.ModelSerializer):
    project = serializers.HyperlinkedRelatedField(
        view_name='project-detail',
        queryset=Project.objects.all()
    )
    assigned_to = serializers.HyperlinkedRelatedField(
        view_name='staff-detail',
        queryset=Staff.objects.all()
    )
    status = serializers.SlugRelatedField(slug_field='title', queryset=Status.objects.all())
    class Meta:
        model = Job
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class StatusGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusGroup
        fields = '__all__'
