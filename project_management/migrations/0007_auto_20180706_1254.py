# Generated by Django 2.0.7 on 2018-07-06 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0006_auto_20180706_1218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='address',
            new_name='addresses',
        ),
    ]
