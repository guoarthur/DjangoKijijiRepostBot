# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-22 22:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poster', '0005_auto_20161222_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='postableitem',
            name='password',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='postableitem',
            name='username',
            field=models.CharField(default='', max_length=40),
            preserve_default=False,
        ),
    ]
