# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from database.models import Tweet
from database.models import Hashtag
from nltk import word_tokenize
from django.http import HttpResponse
import json
from datetime import datetime, timedelta
from django.template.loader import render_to_string


# Create your views here.
class HomePageView(TemplateView):
    num_tweets = 30

    def get(self, request, **kwargs):
        return render(request, 'index.html', self.get_tweets(self.num_tweets))

    def post(self, request, **kwargs):
        tweet_count = int(request.POST.get('num_tweets'))

        graphs_data = render(request, 'graphs.html', self.get_tweets(tweet_count))
        tweet_data = render(request, 'tweets.html', self.get_tweets(tweet_count))

        new_data = {
            'graphs': str(graphs_data),
            'tweets': str(tweet_data)
        }

        return HttpResponse(json.dumps(new_data))

    def clean_tweet(self, tweet):
        clean_tweet = tweet.replace("\n", "").replace("&amp;", "&").replace('"', '\\"')
        clean_tweet = " ".join(clean_tweet.split())

        return clean_tweet

    # Get the recent tweets in the database. The number of tweets returned passed in a parameter.
    # Returns a list containing all the tweets requests
    def get_recent_tweets(self, tweets, tweets_size):
        recent_tweets = []
        count = 0

        for tweet in tweets:
            if not tweet.is_rt and count < tweets_size:
                tweet.tweet_body = self.clean_tweet(tweet.tweet_body)
                recent_tweets.append(tweet)
                count += 1

        return recent_tweets

    def get_top_tweets(self, sortedTweets, tweets_size):
        top_tweets = []
        count = 0

        for tweet in sortedTweets:
            tweet.tweet_body = self.clean_tweet(tweet.tweet_body)
            top_tweets.append(tweet)

            count += 1

            if count == tweets_size:
                break

        return top_tweets

    def get_tweets(self, how_many):
        data = [
            Tweet.objects.filter(sentiment_string="pos").count(),
            Tweet.objects.filter(sentiment_string="neu").count(),
            Tweet.objects.filter(sentiment_string="neg").count()
        ]

        tweets = Tweet.objects.all()

        recent_tweets = self.get_recent_tweets(tweets.order_by("-creation_date"), how_many)

        rtSorted = list(tweets.order_by("-rt_count").filter(is_rt=False))
        rtSorted = rtSorted[:how_many]
        rtSorted = fixNames(rtSorted)

        favSorted = list(tweets.order_by("-fav_count"))
        favSorted = favSorted[:how_many]
        favSorted = fixNames(favSorted)

        repSorted = list(tweets.order_by("-rep_count"))
        repSorted = repSorted[:how_many]
        repSorted = fixNames(repSorted)

        tweets = list(tweets.order_by("-creation_date"))

        for tweet in tweets:
            tweet.tweet_body = self.clean_tweet(tweet.tweet_body)

        topReplyTweet = self.get_top_tweets(repSorted, how_many)
        topFavTweet = self.get_top_tweets(favSorted, how_many)
        topRtTweet = self.get_top_tweets(rtSorted, how_many)

        hashtags = Hashtag.objects.all();

        tweet_data = {'sentimentCounts': data, 'retweetCounts': rtSorted, 'favouriteCounts': favSorted,
                      'replyCounts': repSorted, 'recentTweets': recent_tweets, 'topRetweet': topRtTweet,
                      'topFavorite': topFavTweet, 'topReply': topReplyTweet, 'tweets': tweets, 'hashtags': hashtags}

        return tweet_data


class WordCloudView(TemplateView):
    def get(self, request, **kwargs):
        ignore = ["#", ":", "@", ".", "rt", ",", "and",
                  "the", "yeg", "yegtraffic", "to", "too", "the",
                  "a", "https", "on", "your", "is", "in", "at",
                  "be", "!", "of", "if", "this", ";", "…", "?",
                  "&", "amp", "for", "eb", "nb", "sb", "wb",
                  "are", ")", "(", "i", "from", "'", "as", "...",
                  "-", "via", "n't", "there", "not", "with", "it",
                  "'s", "``", "y…", "2", "can", "re", "an", "has",
                  "go", "my", "was", "do", "//t.co/sy0e4le9ig",
                  "how", "t", "am", "shpk", "here", "s", "//t.co/2i4nbtnm9a",
                  "us", "*k", "u", "//t.co/9j3kp3kcke", "//t.co/col4ejqh…",
                  "w/", "'m", "‘", "'er", "'ve", "-…", "", "st", "street",
                  "ave", "av", "avenue", "you"
                  ]
        tweets = Tweet.objects.all()
        tweet_dict = {}
        result = {}
        for t in tweets:
            words = word_tokenize(t.tweet_body)
            for word in words:
                word = word.encode('ascii', 'ignore')
                if word.lower() not in ignore:
                    if tweet_dict.has_key(word.lower()):
                        tweet_dict[word.lower()] += 1
                    else:
                        tweet_dict[word.lower()] = 1
        for i in range(0, 10):
            key, value = max(tweet_dict.iteritems(), key=lambda p: p[1])
            result[key] = value
            tweet_dict.pop(key, None)
        print type(result)
        return render(request, 'word_cloud.html', {'result': result})


class LineChartView(TemplateView):
    def get(self, request, **kwargs):
        tweets = list(Tweet.objects.all().order_by('tweet_id'))

        return render(request, 'line_chart.html', {'tweets': tweets, 'tweets_length': len(tweets)})


# d3 cannot create two sperate entries for something with the same name.
# Could EASILY become a problem down the line.
def fixNames(tweets):
    usedNames = []
    for item in tweets:
        while usedNames.count(item.user_id.screen_name) >= 1:
            if item.user_id.screen_name in usedNames:
                item.user_id.screen_name = item.user_id.screen_name + " "
        usedNames.append(item.user_id.screen_name)

    return tweets
