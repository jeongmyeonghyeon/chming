# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-15 11:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0014_auto_20170813_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='open_groups', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='joined_groups', to=settings.AUTH_USER_MODEL),
        ),
    ]
