from datetime import timedelta, date

from rest_framework import serializers

from project_management.authority import hyperlinkedRelatedFieldByAuthority, slugRelatedFieldByAuthority
from project_management.models import Staff, StatusGroup, Job, Status, Project, Company, EmailAddress, Address, Client, \
    User, Authority, ScheduledTodo, WorkDay, Todo


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('authority',)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'url', 'clients', 'addresses')
        read_only_fields = ('authority',)

    def get_fields(self):
        fields = super().get_fields()

        authority = self.context['request'].session.get('authority')
        fields['clients'] = hyperlinkedRelatedFieldByAuthority(Client, 'client-detail', authority)
        fields['addresses'] = hyperlinkedRelatedFieldByAuthority(Address, 'address-detail', authority)

        return fields


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('authority',)

    def get_fields(self):
        fields = super().get_fields()

        authority = self.context['request'].session.get('authority')
        fields['email_address'] = slugRelatedFieldByAuthority(EmailAddress, 'email', authority)

        return fields


class EmailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAddress
        fields = '__all__'
        read_only_fields = ('authority',)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ('status_group',)
        read_only_fields = ('authority',)

    def get_fields(self):
        fields = super().get_fields()

        authority = self.context['request'].session.get('authority')
        fields['company'] = hyperlinkedRelatedFieldByAuthority(Company, 'company-detail', authority, False)

        return fields


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ('authority',)


class JobSerializer(serializers.ModelSerializer):
    todo = TodoSerializer()

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('authority',)

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        todo_representation = representation.pop('todo')
        for key in todo_representation:
            representation[key] = todo_representation[key]

        return representation

    def create(self, validated_data):
        todo_data = validated_data.pop('todo')
        todo = Todo(**todo_data)
        todo.save()
        job = Job.objects.create(todo=todo, **validated_data)
        return job


class TaskSerializer(serializers.ModelSerializer):
    todo = TodoSerializer()

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('authority',)

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        todo_representation = representation.pop('todo')
        for key in todo_representation:
            representation[key] = todo_representation[key]

        return representation


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
        read_only_fields = ('authority',)

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
        read_only_fields = ('authority',)


class WorkDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDay
        fields = '__all__'
        read_only_fields = ('authority',)

    def get_fields(self):
        fields = super().get_fields()

        authority = self.context['request'].session.get('authority')
        fields['staff'] = hyperlinkedRelatedFieldByAuthority(Staff, 'staff-detail', authority, False)
        return fields


class ScheduledTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledTodo
        fields = '__all__'
        read_only_fields = ('authority',)

    def get_fields(self):
        fields = super().get_fields()

        authority = self.context['request'].session.get('authority')
        fields['work_day'] = hyperlinkedRelatedFieldByAuthority(WorkDay, 'workday-detail', authority, False)
        fields['todo__assigned_to'] = hyperlinkedRelatedFieldByAuthority(Staff, 'staff-detail', authority, False)
        fields['todo__project'] = hyperlinkedRelatedFieldByAuthority(Project, 'project-detail', authority, False)
        return fields


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'
        read_only_fields = ('authority',)


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
