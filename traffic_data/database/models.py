# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from datetime import datetime
from TwitterSearch import *
import json

# testing something
# Required keys to access the API
key = 'w645Oz4LizFb9bd1UzbAbdzVq'
secret = '9UfawqpsphzYHyjKi6S1j06AyLagDn4EvaXZiVFVeU99KtiG7u'
token_key = '1113900372-SIKdu4TXMdDEpsBBqdIdurWvjH5Mt1SwDaEhAcz'
token_secret = 'YoPJzhZvngJP6KVnW8XZmytU5AH1PZHEJILnb6yYJCLdm'


# Create your models here.

class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    user_name = models.TextField(null=True, default=None)
    total_followers = models.IntegerField(null=True, default=None)
    total_fav = models.IntegerField(null=True, default=None)
    total_following = models.IntegerField(null=True, default=None)
    creation_date = models.DateTimeField(null=True, default=None)
    upload_date = models.DateTimeField(null=True, default=None)
    total_tweets = models.IntegerField(null=True, default=None)

    def __str__(self):  # __unicode__ on Python 2
        return self.upload_date

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


class Tweet(models.Model):
    tweet_id = models.IntegerField(primary_key=True)
    tweet_body = models.TextField(null=True, default=None)
    tweet_url = models.TextField(null=True, default=None)
    creation_date = models.DateTimeField(null=True, default=None)
    upload_date = models.DateTimeField(null=True, default=None)
    rep_count = models.IntegerField(null=True, default=None)
    fav_count = models.IntegerField(null=True, default=None)
    rt_count = models.IntegerField(null=True, default=None)
    tid_parent = models.IntegerField(null=True, default=None)
    lang = models.CharField(null=True, default=None, max_length=10)

    # user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.tweet_body

    # Insert the data in the Tweet table
    @classmethod
    def insert_tweet(cls, tweet_id, tweet_body, tweet_url, creation_data, rep_count, fav_count, rt_count,
                     tid_parent, lang, user_id):
        tweet = Tweet(
            tweet_id=tweet_id,
            tweet_body=tweet_body,
            tweet_url=tweet_url,
            creation_data=format_datetime(creation_data),
            upload_date=timezone.now(),
            rep_count=rep_count,
            fav_count=fav_count,
            rt_count=rt_count,
            tid_parent=tid_parent,
            lang=lang,
            # user_id=user_id
        )
        tweet.save()


class Hashtag(models.Model):
    class Meta:
        unique_together = (('tweet_id', 'hashtag'),)

    tweet_id = models.IntegerField(editable=False, default=None, null=True)
    hashtag = models.CharField(default=None, max_length=255)


def store(hashtags):
    try:
        tso = TwitterSearchOrder()
        tso.set_keywords(hashtags)

        ts = TwitterSearch(
            consumer_key=key,
            consumer_secret=secret,
            access_token=token_key,
            access_token_secret=token_secret
        )
        count = 0
        for tweet in ts.search_tweets_iterable(tso):
            User.insert_user(
                tweet['user']['id'],
                tweet['user']['screen_name'],
                tweet['user']['followers_count'],
                tweet['user']['favourites_count'],
                tweet['user']['friends_count'],
                tweet['user']['created_at'],
                tweet['user']['statuses_count']
            )
            # print 'created_at', tweet['user']['created_at']
            # Tweet.insert_tweet(
            #     tweet['id'],
            #     tweet['text'],
            # )
            # print('%s tweeted: %s' % (tweet['user']['name'], tweet['created_at']))
            # print json.dumps(tweet, sort_keys=True, indent=3, separators=(',', ': '))
            count += 1
            # if count >= 10:
            #     break
            # print count
            break
    except TwitterSearchException as e:  # take care of all those ugly errors if there are some
        print(e)


def format_datetime(datetime):
    datetime_split = datetime.split(" ")
    datetime_format = datetime_split[5] + '-' + convert_month(datetime_split[1]) + '-' + datetime_split[2] + ' ' + \
                      datetime_split[3] + datetime_split[4]
    return datetime_format


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
        return 'NOTHING MATCHED to the month!'


hashtags = ['yegtraffic', 'ABRoads']
store(hashtags)
