# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-09-23 12:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
    ]
