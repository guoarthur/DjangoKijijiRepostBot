# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-24 06:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poster', '0010_auto_20161223_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='postableitem',
            name='repostWaitInterval',
            field=models.IntegerField(default=86400),
        ),
    ]
