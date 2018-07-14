import uuid as uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_project_manager = models.BooleanField(
        default=False,
        help_text='Should this staff member have project management permissions',
    )


class Authority(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    expires_at = models.DateField()
    is_active = models.BooleanField()

    def get_uuid(self):
        return self.uuid.__str__()

    def __str__(self):
        return self.uuid.__str__()


class Address(models.Model):
    class Meta:
        verbose_name_plural = "Addresses"

    address_first_line = models.CharField(max_length=120)
    address_second_line = models.CharField(max_length=120, null=True)
    city = models.CharField(max_length=120)
    county = models.CharField(max_length=120, null=True)
    country = models.CharField(max_length=120, null=True)
    post_code = models.CharField(max_length=10)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, null=True, editable=False)

    def __str__(self):
        return self.authority.get_uuid()


class Client(models.Model):
    fullname = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return self.fullname


class EmailAddress(models.Model):
    class Meta:
        verbose_name_plural = "Email Addresses"

    email = models.EmailField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, related_name='email_addresses', blank=True, null=True)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, null=True, editable=False)

    def __str__(self):
        return self.email


class Company(models.Model):
    class Meta:
        verbose_name_plural = "Companies"

    name = models.CharField(max_length=255)
    addresses = models.ManyToManyField(Address, related_name='addresses')
    clients = models.ManyToManyField(Client, related_name="companies")
    url = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return self.name


class StatusGroup(models.Model):
    title = models.CharField(max_length=30)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, null=True, editable=False)

    def __str__(self):
        return self.title


class Status(models.Model):
    class Meta:
        verbose_name_plural = "Statuses"

    title = models.CharField(max_length=30)
    status_group = models.ForeignKey(StatusGroup, on_delete=models.CASCADE)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return self.title


class Project(models.Model):
    reference_code = models.CharField(max_length=20)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    status_group = models.ForeignKey(StatusGroup, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return self.reference_code


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rate = models.FloatField(default=0)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "staff"

    def __str__(self):
        return self.user.username


class Todo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference_code = models.CharField(max_length=20)
    title = models.CharField(max_length=140)
    description = models.CharField(max_length=255)
    estimated_time = models.FloatField(default=0)
    logged_time = models.FloatField(default=0)
    assigned_to = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, to_field='user')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return "%s: %s" % (self.reference_code, self.title)


class Job(models.Model):
    todo = models.OneToOneField(Todo, on_delete=models.CASCADE, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return str(self.todo)


class Task(models.Model):
    todo = models.OneToOneField(Todo, on_delete=models.CASCADE, primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return str(self.todo)


class WorkDay(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.FloatField()
    repeat = models.IntegerField(default=-1)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return "%s: %s, %sh" % (self.staff, self.date, self.hours)


class ScheduledTodo(models.Model):
    todo = models.OneToOneField(Todo, on_delete=models.CASCADE, primary_key=True)
    work_day = models.ForeignKey(WorkDay, on_delete=models.CASCADE)
    time = models.FloatField()
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return "%s: %s " % (self.todo.title, self.todo.status)
