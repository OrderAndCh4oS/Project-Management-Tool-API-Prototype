# Generated by Django 2.0.7 on 2018-07-06 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0007_auto_20180706_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='town',
        ),
    ]