# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-12-02 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0003_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='receivetime',
            field=models.DateField(verbose_name='接收需求时间'),
        ),
    ]
