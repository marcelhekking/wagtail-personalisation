# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-10 12:39
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0030_index_on_pagerevision_created_at'),
        ('personalisation', '0021_auto_20161110_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitcountrule',
            name='counted_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page'),
        ),
    ]
