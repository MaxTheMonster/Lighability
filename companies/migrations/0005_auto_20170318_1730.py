# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-18 17:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_auto_20170318_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='latitude',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='company',
            name='longitude',
            field=models.IntegerField(default=1),
        ),
    ]
