# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-15 11:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0013_auto_20170812_0003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='open_group',
        ),
    ]
