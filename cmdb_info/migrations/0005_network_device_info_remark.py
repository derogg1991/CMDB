# Generated by Django 2.0 on 2018-09-11 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb_info', '0004_auto_20180911_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='network_device_info',
            name='remark',
            field=models.TextField(default='', verbose_name='备注'),
            preserve_default=False,
        ),
    ]
