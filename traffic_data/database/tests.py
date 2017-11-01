# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from datetime import datetime
from database.models import User, Tweet, Hashtag, format_datetime

# Create your tests here.


class UserModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create(
            user_id=1,
            user_name="user 1",
            total_followers=1,
            total_fav=1,
            total_following=1,
            creation_date=None,
            upload_date=None,
            total_tweets=5
        )

        user_2 = User.objects.create(
            user_id=2,
            user_name="user 2",
            total_followers=2,
            total_fav=2,
            total_following=2,
            creation_date=None,
            upload_date=None,
            total_tweets=10
        )

        Tweet.objects.create(
            tweet_id=1,
            tweet_body="Tweet 1. Positive sentiment.",
            tweet_url=None,
            creation_date=None,
            upload_date=None,
            rep_count=1,
            fav_count=0,
            rt_count=1,
            tid_parent=None,
            lang="eng",
            sentiment=1,
            pos=1,
            neg=0,
            neu=0,
            sentiment_string="pos",
            user_id=user_1
        )

        Hashtag.objects.create(
            tweet_id=1,
            hashtag="positive"
        )

        Hashtag.objects.create(
            tweet_id=1,
            hashtag="goodvibes"
        )

        Tweet.objects.create(
            tweet_id=2,
            tweet_body="Tweet 2. Negative sentiment. Reply to tweet_1",
            tweet_url=None,
            creation_date=None,
            upload_date=None,
            rep_count=0,
            fav_count=5,
            rt_count=3,
            tid_parent=1,
            lang="eng",
            sentiment=-1,
            pos=0,
            neg=0,
            neu=-1,
            sentiment_string="neg",
            user_id=user_2
        )

    def test_user_from_tweet(self):
        tweet = Tweet.objects.get(pk=1)
        user = User.objects.get(pk=1)
        tweet_user = tweet.user_id
        self.assertEquals(tweet_user, user)

    def test_username_from_tweet(self):
        tweet = Tweet.objects.get(pk=1)
        tweet_user_name = tweet.user_id.user_name
        self.assertEquals(tweet_user_name, "user 1")

    def test_hashtags_for_tweet(self):
        tweet = Tweet.objects.get(pk=1)
        tags = Hashtag.objects.filter(tweet_id=1)
        expected = ["goodvibes", "positive"]
        results = []
        for tag in tags:
            results.append(tag.hashtag)
        self.assertEquals(expected, results)
