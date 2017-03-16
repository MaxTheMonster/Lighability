# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-06 15:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='slug',
            field=models.SlugField(default=1, max_length=40, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='time',
            field=models.DateField(default=datetime.datetime(2017, 3, 6, 15, 50, 55, 721830, tzinfo=utc)),
        ),
    ]