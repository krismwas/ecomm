# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2021-06-29 12:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_myuser_full_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='active',
            new_name='is_active',
        ),
    ]