from datetime import timedelta, date

from expander import ExpanderSerializerMixin
from rest_framework import serializers

from project_management.authority import hyperlinkedRelatedFieldByAuthority, slugRelatedFieldByAuthority, \
    get_the_authority
from project_management.models import Staff, StatusGroup, Job, Status, Project, Company, EmailAddress, Address, Client, \
    User, Authority, ScheduledTodo, WorkDay, Todo, Task


class BaseSerializer(ExpanderSerializerMixin, serializers.ModelSerializer):
    pass


class AddressSerializer(BaseSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('authority',)


class ClientSerializer(BaseSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('authority',)

    def get_fields(self):
        fields = super().get_fields()

        authority = get_the_authority(self.context['request'].user)
        fields['email_addresses'] = slugRelatedFieldByAuthority(EmailAddress, 'email', authority, True)

        return fields


class CompanySerializer(BaseSerializer):
    class Meta:
        model = Company
        fields = ('name', 'url', 'clients', 'addresses')
        read_only_fields = ('authority',)
        expandable_fields = {
            'clients': (ClientSerializer, (), {'many': True}),
            'addresses': (AddressSerializer, (), {'many': True})
        }

    def get_fields(self):
        fields = super().get_fields()

        authority = get_the_authority(self.context['request'].user)
        fields['clients'] = hyperlinkedRelatedFieldByAuthority(Client, 'client-detail', authority)
        fields['addresses'] = hyperlinkedRelatedFieldByAuthority(Address, 'address-detail', authority)

        return fields


class EmailAddressSerializer(BaseSerializer):
    class Meta:
        model = EmailAddress
        fields = '__all__'
        read_only_fields = ('authority',)


class ProjectSerializer(BaseSerializer):
    class Meta:
        model = Project
        exclude = ('status_group',)
        read_only_fields = ('authority',)
        expandable_fields = {
            'company': CompanySerializer,
        }

    def get_fields(self):
        fields = super().get_fields()

        authority = get_the_authority(self.context['request'].user)
        fields['company'] = hyperlinkedRelatedFieldByAuthority(Company, 'company-detail', authority, False)

        return fields


class TodoSerializer(BaseSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ('authority',)


class JobSerializer(BaseSerializer):
    todo = TodoSerializer()


    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('authority',)
        expandable_fields = {
            'project': ProjectSerializer,
        }

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        todo_representation = representation.pop('todo')
        for key in todo_representation:
            representation[key] = todo_representation[key]

        return representation

    def create(self, validated_data):
        todo_data = validated_data.pop('todo')
        authority = Authority.objects.get(uuid=get_the_authority(self.context['request'].user))

        todo = Todo(**todo_data)
        todo.authority = authority
        todo.save()
        job = Job.objects.create(todo=todo, **validated_data)
        return job


class TaskSerializer(BaseSerializer):
    todo = TodoSerializer()

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('authority',)
        expandable_fields = {
            'job': JobSerializer,
        }

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        todo_representation = representation.pop('todo')
        for key in todo_representation:
            representation[key] = todo_representation[key]

        return representation

    def create(self, validated_data):
        todo_data = validated_data.pop('todo')
        authority = Authority.objects.get(uuid=get_the_authority(self.context['request'].user))

        todo = Todo(**todo_data)
        todo.authority = authority
        todo.save()
        task = Task.objects.create(todo=todo, **validated_data)

        return task


class UserSerializer(BaseSerializer):
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


class StaffSerializer(BaseSerializer):
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


class StatusGroupSerializer(BaseSerializer):
    class Meta:
        model = StatusGroup
        fields = '__all__'
        read_only_fields = ('authority',)


class WorkDaySerializer(BaseSerializer):
    class Meta:
        model = WorkDay
        fields = '__all__'
        read_only_fields = ('authority',)
        expandable_fields = {
            'staff': StaffSerializer,
        }

    def get_fields(self):
        fields = super().get_fields()

        authority = get_the_authority(self.context['request'].user)
        fields['staff'] = hyperlinkedRelatedFieldByAuthority(Staff, 'staff-detail', authority, False)
        return fields


class ScheduledTodoSerializer(BaseSerializer):
    # Todo: Rework polymorphic relations using generic serializer or what ever it is
    class Meta:
        model = ScheduledTodo
        fields = '__all__'
        read_only_fields = ('authority',)
        expandable_fields = {
            'work_day': WorkDaySerializer,
            'todo': TodoSerializer,
        }

    def get_fields(self):
        fields = super().get_fields()

        authority = get_the_authority(self.context['request'].user)
        fields['work_day'] = hyperlinkedRelatedFieldByAuthority(WorkDay, 'workday-detail', authority, False)
        return fields


class StatusSerializer(BaseSerializer):
    class Meta:
        model = Status
        fields = '__all__'
        read_only_fields = ('authority',)


class CreateUserSerializer(BaseSerializer):
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
