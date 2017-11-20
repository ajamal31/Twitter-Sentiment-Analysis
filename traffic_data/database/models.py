# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.shortcuts import get_list_or_404, get_object_or_404


# Create your models here.

# User table and the method that we need for it
class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True, default=0)
    user_name = models.TextField(null=True, default=None)
    total_followers = models.IntegerField(null=True, default=None)
    total_fav = models.IntegerField(null=True, default=None)
    total_following = models.IntegerField(null=True, default=None)
    creation_date = models.DateTimeField(null=True, default=None)
    upload_date = models.DateTimeField(null=True, default=None)
    total_tweets = models.IntegerField(null=True, default=None)

    def __str__(self):
        return str(self.user_name)

    # Add the data in the User table
    @classmethod
    def insert_user(cls, user_id, user_name, total_followers, total_fav, total_following, creation_date, total_tweets):
        user = User(
            user_id=user_id,
            user_name=user_name,
            total_followers=total_followers,
            total_fav=total_fav,
            total_following=total_following,
            creation_date=format_datetime(creation_date),
            upload_date=timezone.now(),
            total_tweets=total_tweets
        )

        user.save()


# Tweet table and the method that we need for it
class Tweet(models.Model):
    tweet_id = models.BigIntegerField(primary_key=True, default=0)
    tweet_body = models.CharField(null=True, default=None, max_length=140)
    tweet_url = models.TextField(null=True, default=None)
    creation_date = models.DateTimeField(null=True, default=None)
    upload_date = models.DateTimeField(null=True, default=None)
    rep_count = models.IntegerField(null=True, default=None)
    fav_count = models.IntegerField(null=True, default=None)
    rt_count = models.IntegerField(null=True, default=None)
    tid_parent = models.BigIntegerField(null=True, default=None)
    lang = models.CharField(null=True, default=None, max_length=10)
    # Compound field returned from VADER
    sentiment = models.FloatField(null=True, default=None)
    # The pos, neu, and neg scores are ratios for proportions of text that fall in each category
    pos = models.FloatField(null=True, default=None)
    neu = models.FloatField(null=True, default=None)
    neg = models.FloatField(null=True, default=None)
    # A string summarizing sentiment of tweet_body.
    # Positive if sentiment >= 0.5, negative if sentiment <=-0.5. Neutral otherwise.
    # Breakpoints taken from VADER documentation.
    sentiment_string = models.CharField(null=True, default=None, max_length=5)
    is_rt = models.BooleanField(default=False)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return str(self.tweet_id)

    # Insert the data in the Tweet table
    @classmethod
    def insert_tweet(cls, tweet_id, tweet_body, creation_date, fav_count, rt_count,
                     tid_parent, lang, user_id, sentiment, pos, neg, neu, sentiment_string, is_rt):
        tweet = Tweet(
            tweet_id=tweet_id,
            tweet_body=tweet_body,
            creation_date=format_datetime(creation_date),
            fav_count=fav_count,
            rt_count=rt_count,
            tid_parent=tid_parent,
            lang=lang,
            user_id=user_id,
            upload_date=timezone.now(),
            sentiment=sentiment,
            pos=pos,
            neg=neg,
            neu=neu,
            sentiment_string=sentiment_string,
            is_rt=is_rt
        )

        tweet.save()

    # Insert the reply count data in the Tweet table
    @classmethod
    def insert_replycount(cls, tw_id, reply_count):
        tweet_object = get_object_or_404(Tweet, pk=tw_id)  # get object by tweet_id
        tweet_object.rep_count = reply_count

        tweet_object.save(update_fields=["rep_count"])


# Hashtag table and the method that we need for it
class Hashtag(models.Model):
    tweet_id = models.BigIntegerField(editable=False, default=None, null=True)
    hashtag = models.CharField(default=None, max_length=255, null=True)

    # The attributes below need to be unique to avoid duplicates
    class Meta:
        unique_together = ["tweet_id", "hashtag"]

    def __str__(self):
        return str(self.tweet_id)

    # Insert the data in the table
    @classmethod
    def insert_hashtag(cls, tweet_id, hashtag):
        if not Hashtag.objects.filter(tweet_id=tweet_id, hashtag=hashtag):
            hashtag = Hashtag(
                tweet_id=tweet_id,
                hashtag=hashtag
            )

            hashtag.save()


# Format's the datetime to match the format of the database's datetime field
def format_datetime(datetime):
    datetime_split = datetime.split(" ")
    datetime_format = datetime_split[5] + '-' + convert_month(datetime_split[1]) + '-' + datetime_split[2] + ' ' + \
                      datetime_split[3] + datetime_split[4]
    return datetime_format


# Converts the letter version of the month to its digits
def convert_month(month):
    if month == 'Jan':
        return '01'
    elif month == 'Feb':
        return '02'
    elif month == 'Mar':
        return '03'
    elif month == 'Apr':
        return '04'
    elif month == 'May':
        return '05'
    elif month == 'Jun':
        return '06'
    elif month == 'Jul':
        return '07'
    elif month == 'Aug':
        return '08'
    elif month == 'Sep':
        return '09'
    elif month == 'Oct':
        return '10'
    elif month == 'Nov':
        return '11'
    elif month == 'Dec':
        return '12'
    else:
        return ''
