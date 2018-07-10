from django.contrib import admin

from project_management import models

admin.site.register(models.Address)
admin.site.register(models.EmailAddress)
admin.site.register(models.Client)
admin.site.register(models.Company)
admin.site.register(models.StatusGroup)
admin.site.register(models.Status)
admin.site.register(models.Project)
admin.site.register(models.Job)
admin.site.register(models.Staff)
