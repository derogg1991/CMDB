# Generated by Django 2.0 on 2018-09-11 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb_info', '0003_auto_20180911_1525'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pc_info',
            old_name='creat_date',
            new_name='create_date',
        ),
        migrations.RenameField(
            model_name='pc_info',
            old_name='localtion',
            new_name='location',
        ),
        migrations.RenameField(
            model_name='server_info',
            old_name='localtion',
            new_name='location',
        ),
    ]
