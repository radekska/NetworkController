# Generated by Django 3.1.1 on 2020-10-22 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_app', '0007_auto_20201022_1525'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deviceinterface',
            old_name='lldp_neighbor_interace',
            new_name='lldp_neighbor_interface',
        ),
    ]
