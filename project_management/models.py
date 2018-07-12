import uuid as uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_project_manager = models.BooleanField(
        default=False,
        help_text=('Should this staff member have project management permissions'),
    )


# ToDo: Workout how to serialize objects correctly
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


class EmailAddress(models.Model):
    class Meta:
        verbose_name_plural = "Email Addresses"

    email = models.EmailField(max_length=255)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, null=True, editable=False)

    def __str__(self):
        return self.email


class Client(models.Model):
    fullname = models.CharField(max_length=80)
    email_address = models.ForeignKey(EmailAddress, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return self.fullname


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
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, null=True, blank=True)
    rate = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = "staff"

    def __str__(self):
        return self.user.username


class Job(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    reference_code = models.CharField(max_length=20)
    title = models.CharField(max_length=140)
    description = models.CharField(max_length=255)
    deadline = models.DateTimeField(null=True)
    estimated_time = models.FloatField(default=0)
    logged_time = models.FloatField(default=0)
    assigned_to = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, to_field='user')
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE, editable=False)

    def __str__(self):
        return self.title
