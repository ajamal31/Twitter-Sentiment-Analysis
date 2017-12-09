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
    default_min_date = datetime(2013, 9, 30, 7, 6, 5)
    default_max_date = datetime(3030, 9, 30, 7, 6, 5)

    def get(self, request, **kwargs):
        return render(request, 'index.html',
                      self.get_tweets(self.num_tweets, self.default_min_date, self.default_max_date))

    def post(self, request, **kwargs):
        min_date_str = request.POST.get('min_date')
        min_date_str = min_date_str[:24]

        max_date_str = request.POST.get('max_date')
        max_date_str = max_date_str[:24]

        min_date = datetime.strptime(min_date_str, "%a %b %d %Y %H:%M:%S")
        max_date = datetime.strptime(max_date_str, "%a %b %d %Y %H:%M:%S")

        data = self.get_tweets(self.num_tweets, min_date, max_date)

        bar_data = render(request, 'graphs.html', data)
        line_data = render(request, 'line_chart.html', data)
        tweet_data = render(request, 'tweets.html', data)

        new_data = {
            'bar': str(bar_data)[38:],
            'line': str(line_data)[38:],
            'tweet': str(tweet_data)[38]
        }

        response = HttpResponse(json.dumps(new_data))

        return response

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

    def get_tweets(self, how_many, min_date, max_date):
        tweets = Tweet.objects.all()
        tweets = tweets.filter(creation_date__gt=min_date)
        tweets = tweets.filter(creation_date__lt=max_date)

        data = [
            tweets.filter(sentiment_string="pos").count(),
            tweets.filter(sentiment_string="neu").count(),
            tweets.filter(sentiment_string="neg").count()
        ]

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

        if (len(tweets) > 0):
            latest = tweets[0].creation_date
            earliest = tweets[-1].creation_date
        else:
            latest = datetime.now()
            earliest = datetime.now()

        tweet_data = {'sentimentCounts': data, 'retweetCounts': rtSorted, 'favouriteCounts': favSorted,
                      'replyCounts': repSorted, 'recentTweets': recent_tweets, 'topRetweet': topRtTweet,
                      'topFavorite': topFavTweet, 'topReply': topReplyTweet, 'tweets': tweets,
                      'min_date': earliest, 'max_date': latest}
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
