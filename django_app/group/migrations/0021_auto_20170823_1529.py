# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-23 06:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0020_auto_20170818_1512'),
    ]

    operations = [
        migrations.RenameField(
            model_name='region',
            old_name='dong',
            new_name='level1',
        ),
        migrations.RenameField(
            model_name='region',
            old_name='gu',
            new_name='level2',
        ),
        migrations.RenameField(
            model_name='region',
            old_name='si',
            new_name='level3',
        ),
    ]
