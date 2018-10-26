# Generated by Django 2.0 on 2018-09-11 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_type_text', models.CharField(max_length=400, verbose_name='设备类型')),
            ],
            options={
                'verbose_name_plural': '设备类型',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_text', models.CharField(max_length=400, verbose_name='存放地点')),
            ],
            options={
                'verbose_name_plural': '使用/存放地点',
            },
        ),
        migrations.CreateModel(
            name='Producter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producter_text', models.CharField(max_length=400, verbose_name='品牌型号')),
            ],
            options={
                'verbose_name_plural': '品牌型号',
            },
        ),
    ]
