# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-14 01:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet_id', models.IntegerField(default=None, editable=False, null=True)),
                ('hashtag', models.CharField(default=None, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('tweet_id', models.IntegerField(primary_key=True, serialize=False)),
                ('tweet_body', models.TextField(default=None, null=True)),
                ('tweet_url', models.TextField(default=None, null=True)),
                ('creation_date', models.DateTimeField(default=None, null=True)),
                ('upload_date', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('rep_count', models.IntegerField(default=None, null=True)),
                ('fav_count', models.IntegerField(default=None, null=True)),
                ('rt_count', models.IntegerField(default=None, null=True)),
                ('tid_parent', models.IntegerField(default=None, null=True)),
                ('lang', models.CharField(default=None, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_name', models.TextField(default=None, null=True)),
                ('total_rep', models.IntegerField(default=None, null=True)),
                ('total_fav', models.IntegerField(default=None, null=True)),
                ('total_rt', models.IntegerField(default=None, null=True)),
                ('creation_date', models.DateTimeField(default=None, null=True)),
                ('upload_date', models.DateTimeField(default=datetime.datetime.now, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='tweet',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.User'),
        ),
        migrations.AlterUniqueTogether(
            name='hashtag',
            unique_together=set([('tweet_id', 'hashtag')]),
        ),
    ]
