# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-22 21:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poster', '0004_auto_20161222_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postableattr',
            name='related_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attr', to='poster.PostableItem'),
        ),
    ]
