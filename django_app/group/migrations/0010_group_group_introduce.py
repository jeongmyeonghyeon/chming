# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-11 15:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0009_auto_20170812_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='group_introduce',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]