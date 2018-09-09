from datetime import timedelta, date

from expander import ExpanderSerializerMixin
from rest_framework import serializers
from rest_framework.relations import Hyperlink

from project_management.authority import hyperlinkedRelatedFieldByAuthority, slugRelatedFieldByAuthority, \
    get_the_authority
from project_management.models import Staff, StatusGroup, Status, Project, Company, EmailAddress, Address, Client, \
    User, Authority, ScheduledTodo, WorkDay, Todo, Task, Job


def lift_hyperlinks(dictionary):
    hyperlinks = {}
    if isinstance(dictionary, dict):
        for key, value in list(dictionary.items()):
            if isinstance(value, Hyperlink):
                hyperlinks[key] = dictionary.pop(key)
            elif isinstance(value, list):
                hyperlinks[key] = [hyperlink for hyperlink in value if isinstance(hyperlink, Hyperlink)]
                if len(hyperlinks[key]):
                    del dictionary[key]
                else:
                    del hyperlinks[key]
            else:
                lift_hyperlinks(dictionary[key])
        dictionary['hyperlinks'] = hyperlinks


class GroupHyperlinksSerializer(serializers.Serializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        lift_hyperlinks(representation)

        return representation


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


class CompanySerializer(GroupHyperlinksSerializer, BaseSerializer):
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


class EmailAddressSerializer(GroupHyperlinksSerializer, BaseSerializer):
    class Meta:
        model = EmailAddress
        fields = '__all__'
        read_only_fields = ('authority',)

    def get_fields(self):
        fields = super().get_fields()

        authority = get_the_authority(self.context['request'].user)
        fields['client'] = hyperlinkedRelatedFieldByAuthority(Client, 'client-detail', authority, False)

        return fields


class ProjectSerializer(GroupHyperlinksSerializer, BaseSerializer):
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context['request'].method == 'POST':
            representation['company'] = {'name': instance.company.name}

        return representation


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


class StatusSerializer(GroupHyperlinksSerializer, BaseSerializer):
    class Meta:
        model = Status
        fields = '__all__'
        read_only_fields = ('authority',)

    def get_fields(self):
        fields = super().get_fields()

        authority = get_the_authority(self.context['request'].user)
        fields['status_group'] = hyperlinkedRelatedFieldByAuthority(Project, 'project-detail', authority, False)

        return fields


class TodoSerializer(BaseSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ('authority',)

    def get_fields(self):
        fields = super().get_fields()

        authority = get_the_authority(self.context['request'].user)
        fields['assigned_to'] = hyperlinkedRelatedFieldByAuthority(Staff, 'staff-detail', authority, False)
        fields['status'] = hyperlinkedRelatedFieldByAuthority(Status, 'status-detail', authority, False)

        return fields


class JobSerializer(BaseSerializer):
    todo = TodoSerializer()

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('authority',)
        expandable_fields = {
            'project': ProjectSerializer,
        }

    def get_fields(self):
        fields = super().get_fields()

        authority = get_the_authority(self.context['request'].user)
        fields['project'] = hyperlinkedRelatedFieldByAuthority(Project, 'project-detail', authority, False)

        return fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        todo_representation = representation.pop('todo')
        for key in todo_representation:
            representation[key] = todo_representation[key]

        representation['project__title'] = instance.project.title
        representation['status__title'] = instance.todo.status.title
        representation['assigned_to__username'] = instance.todo.assigned_to.user.username

        project = representation.pop('project')
        status = representation.pop('status')
        assigned_to = representation.pop('assigned_to')

        representation['hyperlinks'] = {
            "project": project,
            "status": status,
            "assigned_to": assigned_to
        }

        return representation

    def to_internal_value(self, data):
        todo_internal = {}
        for key in TodoSerializer.Meta.fields:
            if key in data:
                todo_internal[key] = data.pop(key)

        internal = super().to_internal_value(data)
        internal['todo'] = todo_internal
        return internal

    def update(self, instance, validated_data):
        todo_data = validated_data.pop('todo')
        super().update(instance, validated_data)

        todo = instance.todo
        for attr, value in todo_data.items():
            setattr(todo, attr, value)
        todo.save()

        return instance

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        todo_representation = representation.pop('todo')
        for key in todo_representation:
            representation[key] = todo_representation[key]

        representation['job__title'] = instance.job.todo.title
        representation['status__title'] = instance.todo.status.title
        representation['assigned_to__username'] = instance.todo.assigned_to.user.username

        job = representation.pop('job')
        status = representation.pop('status')
        assigned_to = representation.pop('assigned_to')

        representation['hyperlinks'] = {
            "job": job,
            "status": status,
            "assigned_to": assigned_to
        }

        return representation

    def create(self, validated_data):
        todo_data = validated_data.pop('todo')
        authority = Authority.objects.get(uuid=get_the_authority(self.context['request'].user))

        todo = Todo(**todo_data)
        todo.authority = authority
        todo.save()
        task = Task.objects.create(todo=todo, **validated_data)

        return task


class WorkDaySerializer(GroupHyperlinksSerializer, BaseSerializer):
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


class ScheduledTodoSerializer(GroupHyperlinksSerializer, BaseSerializer):
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
