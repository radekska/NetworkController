# Generated by Django 3.1.1 on 2020-10-12 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_app', '0002_devicemodel_system_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicemodel',
            name='device_os',
        ),
    ]