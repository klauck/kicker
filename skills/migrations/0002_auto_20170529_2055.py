# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 20:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='trueskill_gamma',
            new_name='trueskill_mu',
        ),
    ]
