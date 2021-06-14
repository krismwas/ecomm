# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2021-06-09 11:33
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, upload_to=products.models.upload_image_path),
        ),
    ]