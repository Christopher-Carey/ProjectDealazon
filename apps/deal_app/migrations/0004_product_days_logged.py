# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-10-23 21:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deal_app', '0003_deal'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='days_logged',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
