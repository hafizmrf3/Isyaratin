# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-28 16:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mycollections', '0002_auto_20190128_1922'),
    ]

    operations = [
        migrations.RenameField(
            model_name='signlanguage',
            old_name='signlanguage_logo',
            new_name='logo',
        ),
        migrations.RenameField(
            model_name='signlanguage',
            old_name='signlanguage_name',
            new_name='name',
        ),
    ]
