# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from TwitterSearch import *

# Required keys to access the API
key = 'w645Oz4LizFb9bd1UzbAbdzVq'
secret = '9UfawqpsphzYHyjKi6S1j06AyLagDn4EvaXZiVFVeU99KtiG7u'
token_key = '1113900372-SIKdu4TXMdDEpsBBqdIdurWvjH5Mt1SwDaEhAcz'
token_secret = 'YoPJzhZvngJP6KVnW8XZmytU5AH1PZHEJILnb6yYJCLdm'


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

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return str(self.tweet_id)

    # Insert the data in the Tweet table
    @classmethod
    def insert_tweet(cls, tweet_id, tweet_body, creation_date, fav_count, rt_count, tid_parent, lang, user_id):
        tweet = Tweet(
            tweet_id=tweet_id,
            tweet_body=tweet_body,
            creation_date=format_datetime(creation_date),
            fav_count=fav_count,
            rt_count=rt_count,
            tid_parent=tid_parent,
            lang=lang,
            # user_id=user_id,
            upload_date=timezone.now()
        )

        tweet.save()


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


# Function responsible for making the api calls and storing the data.
def store(tags):
    try:
        # Provides the wrapper with the necessary data for making the calls and retrieving the data
        tso = TwitterSearchOrder()
        tso.set_keywords(tags)

        ts = TwitterSearch(
            consumer_key=key,
            consumer_secret=secret,
            access_token=token_key,
            access_token_secret=token_secret
        )

        count = 0

        for tweet in ts.search_tweets_iterable(tso):

            count += 1

            User.insert_user(
                tweet['user']['id'],
                tweet['user']['screen_name'],
                tweet['user']['followers_count'],
                tweet['user']['favourites_count'],
                tweet['user']['friends_count'],
                tweet['user']['created_at'],
                tweet['user']['statuses_count']
            )

            Tweet.insert_tweet(
                tweet['id'],
                tweet['text'],
                tweet['created_at'],
                tweet['favorite_count'],
                tweet['retweet_count'],
                tweet['in_reply_to_status_id'],
                tweet['lang'],
                tweet['user']['id']
            )

            hashtags_list = tweet['entities']['hashtags']

            # Add the hashtags and duplicates are not added
            for hashtag in hashtags_list:
                Hashtag.insert_hashtag(tweet['id'], (hashtag['text'].lower()))

            # Stop after 200 tweets but this will be removed
            if count >= 200:
                break

        print 'tweet count:', count

    except TwitterSearchException as e:  # take care of all those ugly errors if there are some
        print(e)


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


# I added this for debugging purposes before but this can go if it's not needed
def print_user(tweet):
    print ('id:', tweet['user']['id'], 'screen name:', tweet['user']['screen_name'], 'followers_count:',
           tweet['user']['followers_count'], 'favourites_count:', tweet['user']['favourites_count'], 'friends_count:',
           tweet['user']['friends_count'], 'created_at:', tweet['user']['created_at'], 'statuses_count:',
           tweet['user']['statuses_count'])
    print ''


# These need to be in the controller not here but it's here for testing.
hashtags = ['yegtraffic']
print "Getting data and storing it..."
store(hashtags)
print("Data stored")
