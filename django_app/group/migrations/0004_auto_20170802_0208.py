# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 17:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_auto_20170801_1315'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='modified_date',
        ),
        migrations.AddField(
            model_name='group',
            name='modified_d_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
