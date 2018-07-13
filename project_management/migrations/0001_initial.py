# Generated by Django 2.0.7 on 2018-07-13 10:13

import uuid

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_project_manager', models.BooleanField(default=False,
                                                           help_text='Should this staff member have project management permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_first_line', models.CharField(max_length=120)),
                ('address_second_line', models.CharField(max_length=120, null=True)),
                ('city', models.CharField(max_length=120)),
                ('county', models.CharField(max_length=120, null=True)),
                ('country', models.CharField(max_length=120, null=True)),
                ('post_code', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='Authority',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('expires_at', models.DateField()),
                ('is_active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=80)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('authority', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE,
                                                to='project_management.Authority')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('addresses', models.ManyToManyField(related_name='addresses', to='project_management.Address')),
                ('authority', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE,
                                                to='project_management.Authority')),
                ('clients', models.ManyToManyField(related_name='companies', to='project_management.Client')),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='EmailAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
                ('authority', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE,
                                                to='project_management.Authority')),
            ],
            options={
                'verbose_name_plural': 'Email Addresses',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_code', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('authority', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE,
                                                to='project_management.Authority')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project_management.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('authority', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE,
                                                to='project_management.Authority')),
            ],
            options={
                'verbose_name_plural': 'Statuses',
            },
        ),
        migrations.CreateModel(
            name='StatusGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('authority', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE,
                                                to='project_management.Authority')),
            ],
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reference_code', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=140)),
                ('description', models.CharField(max_length=255)),
                ('estimated_time', models.FloatField(default=0)),
                ('logged_time', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('repeat', models.BooleanField()),
                ('authority', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE,
                                                to='project_management.Authority')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('todo',
                 models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False,
                                      to='project_management.Todo')),
                ('authority', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE,
                                                to='project_management.Authority')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduledTodo',
            fields=[
                ('todo',
                 models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False,
                                      to='project_management.Todo')),
                ('time', models.FloatField()),
                ('status', models.IntegerField(choices=[(0, 'todo'), (1, 'complete')])),
                ('authority', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE,
                                                to='project_management.Authority')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('rate', models.FloatField(default=0)),
                ('authority', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                                to='project_management.Authority')),
            ],
            options={
                'verbose_name_plural': 'staff',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('todo',
                 models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False,
                                      to='project_management.Todo')),
                ('authority', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE,
                                                to='project_management.Authority')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_management.Job')),
            ],
        ),
        migrations.AddField(
            model_name='todo',
            name='authority',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE,
                                    to='project_management.Authority'),
        ),
        migrations.AddField(
            model_name='todo',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_management.Project'),
        ),
        migrations.AddField(
            model_name='todo',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='project_management.Status'),
        ),
        migrations.AddField(
            model_name='status',
            name='status_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_management.StatusGroup'),
        ),
        migrations.AddField(
            model_name='project',
            name='status_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project_management.StatusGroup'),
        ),
        migrations.AddField(
            model_name='client',
            name='email_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project_management.EmailAddress'),
        ),
        migrations.AddField(
            model_name='address',
            name='authority',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='project_management.Authority'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='workday',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_management.Staff'),
        ),
        migrations.AddField(
            model_name='todo',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project_management.Staff'),
        ),
        migrations.AddField(
            model_name='scheduledtodo',
            name='work_day',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_management.WorkDay'),
        ),
    ]
