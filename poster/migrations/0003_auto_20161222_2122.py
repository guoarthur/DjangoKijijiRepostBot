# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-22 21:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poster', '0002_auto_20161222_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostableAttr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=500)),
                ('val', models.CharField(max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name='postableitem',
            name='attr1',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='postableitem',
            name='attr2',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='postableattr',
            name='related_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attrMap', to='poster.PostableItem'),
        ),
    ]