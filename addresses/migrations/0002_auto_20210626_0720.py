# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2021-06-26 07:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adress',
            name='country',
            field=models.CharField(default='United States of America', max_length=120),
        ),
    ]