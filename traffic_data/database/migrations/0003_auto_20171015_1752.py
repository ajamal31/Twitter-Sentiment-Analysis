# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-15 17:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_remove_tweet_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='user',
            name='total_fav',
        ),
        migrations.RemoveField(
            model_name='user',
            name='total_rep',
        ),
        migrations.RemoveField(
            model_name='user',
            name='total_rt',
        ),
        migrations.RemoveField(
            model_name='user',
            name='upload_date',
        ),
    ]
