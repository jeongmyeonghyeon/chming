# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-31 06:36
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_auto_20170727_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_day',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(31)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_month',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(12)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_year',
            field=models.IntegerField(default=2000, validators=[django.core.validators.MaxValueValidator(9999)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('f', 'Female'), ('m', 'Male')], default='f', max_length=1),
            preserve_default=False,
        ),
    ]
