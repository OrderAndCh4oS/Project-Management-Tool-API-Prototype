from django.contrib.auth.models import User
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
        'id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'date_joined')
        read_only_fields = ('is_active', 'is_staff', 'date_joined')
        extra_kwargs = {'password': {'write_only': True}}


class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Staff
        fields = '__all__'

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        user_representation = representation.pop('user')
        for key in user_representation:
            representation[key] = user_representation[key]

        return representation

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User(
            email=user_data['email'],
            username=user_data['username'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        user.set_password(user_data['password'])
        user.is_staff = True
        user.save()
        staff = Staff.objects.create(user=user, **validated_data)
        return staff


class StatusGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusGroup
        fields = '__all__'
