# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 13:12
from __future__ import unicode_literals

from django.db import migrations, models
import member.models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0008_auto_20170807_1936'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', member.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='hobby',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=24, unique=True),
        ),
    ]
