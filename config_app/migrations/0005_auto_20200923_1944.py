# Generated by Django 3.1.1 on 2020-09-23 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config_app', '0004_auto_20200923_1944'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NetworkDeviceSystem',
            new_name='DeviceSystem',
        ),
        migrations.RenameModel(
            old_name='NetworkDeviceUser',
            new_name='DeviceUser',
        ),
    ]
