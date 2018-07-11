from datetime import timedelta, date

from rest_framework import serializers

from project_management.models import Staff, StatusGroup, Job, Status, Project, Company, EmailAddress, Address, Client, \
    User, Authority


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


class EmailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAddress
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
            'id', 'username', 'password',
            'first_name', 'last_name', 'email',
            'is_active', 'is_project_manager',
            'date_joined'
        )
        read_only_fields = ('date_joined',)
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
        password = user_data.pop('password')
        user = User(**user_data)
        user.set_password(password)
        user.save()
        staff = Staff.objects.create(user=user, **validated_data)
        return staff


class StatusGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusGroup
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_project_manager=True,
        )
        user.set_password(validated_data['password'])
        user.save()
        expiry = date.today() + timedelta(days=365)
        authority = Authority.objects.create(expires_at=expiry, is_active=True)

        Staff.objects.create(rate=0, user=user, authority=authority)

        return user
