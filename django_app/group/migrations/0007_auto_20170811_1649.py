# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-11 07:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0006_auto_20170809_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='lat',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='region',
            name='lng',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
        ),
    ]
