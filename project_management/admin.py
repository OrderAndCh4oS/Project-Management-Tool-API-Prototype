from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin

from project_management.models import Address, EmailAddress, Client, Company, Project, Status, Job, StatusGroup, Staff, \
    User

admin.site.register(User, UserAdmin)
admin.site.register(Address)
admin.site.register(EmailAddress)
admin.site.register(Client)
admin.site.register(Company)
admin.site.register(StatusGroup)
admin.site.register(Status)
admin.site.register(Project)
admin.site.register(Job)
admin.site.register(Staff)
