# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-18 06:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0014_remove_user_open_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=24),
        ),
    ]
