# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-06 19:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0003_auto_20180103_2225'),
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin', models.DateField()),
                ('end', models.DateField()),
            ],
        ),
    ]
