# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-06 11:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0008_auto_20170401_1040'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='foursquare_id',
            new_name='api_id',
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.FileField(default='../static/img/profile.jpg', upload_to='profile_pictures/'),
        ),
    ]
