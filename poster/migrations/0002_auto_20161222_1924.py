# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-22 19:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poster', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postableitem',
            name='pmtType',
        ),
        migrations.AddField(
            model_name='postableitem',
            name='adType',
            field=models.CharField(choices=[('O', 'OFFER'), ('W', 'WANTED')], default='O', max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='postableitem',
            name='priceType',
            field=models.CharField(choices=[('F', 'FIXED'), ('GA', 'GIVE_AWAY'), ('C', 'CONTACT'), ('ST', 'SWAP_TRADE')], max_length=1),
        ),
    ]