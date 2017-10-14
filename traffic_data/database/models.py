# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime

# Create your models here.

class User(models.Model):
	user_id = models.IntegerField(primary_key=True)
	user_name = models.TextField(null=True, default=None)
	total_rep = models.IntegerField(null=True, default=None)
	total_fav = models.IntegerField(null=True, default=None)
	total_rt = models.IntegerField(null=True, default=None)
	creation_date = models.DateTimeField(null=True, default=None)
	upload_date = models.DateTimeField(null=True, default=datetime.now)

class Tweet(models.Model):
	tweet_id = models.IntegerField(primary_key=True)
	tweet_body = models.TextField(null=True, default=None)
	tweet_url = models.TextField(null=True, default=None)
	creation_date = models.DateTimeField(null=True, default=None)
	upload_date = models.DateTimeField(null=True, default=datetime.now)
	rep_count = models.IntegerField(null=True, default=None)
	fav_count = models.IntegerField(null=True, default=None)
	rt_count = models.IntegerField(null=True, default=None)
	tid_parent = models.IntegerField(null=True, default=None)
	lang = models.CharField(null=True, default=None, max_length=10)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Hashtag(models.Model):
	class Meta:
		unique_together = (('tweet_id', 'hashtag'),)

	tweet_id = models.IntegerField(editable=False, default=None, null=True)
	hashtag = models.CharField(default=None, max_length=255)