# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 12:32
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_day',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(31)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_month',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(12)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='birth_year',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(9999)]),
        ),
    ]
