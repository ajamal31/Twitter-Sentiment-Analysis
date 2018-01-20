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
from django.utils import timezone
import pytz

timezone.now()
local_timezone = pytz.timezone('America/Edmonton')


# Create your views here.
class HomePageView(TemplateView):
    num_tweets = 30
    default_min_date = datetime(2017, 12, 18, 7, 6, 5, 000000, tzinfo=local_timezone)
    default_max_date = datetime(2017, 12, 25, 7, 6, 5, 000000, tzinfo=local_timezone)
    default_hashtag = 'All'

    def get(self, request, **kwargs):

        most_recent_date = Tweet.objects.all().order_by('-creation_date')[0].creation_date
        week_before_date = most_recent_date - timedelta(days=7)

        return render(request, 'index.html',
                      self.get_tweets(self.num_tweets, week_before_date, most_recent_date,
                                      self.default_hashtag))

    def post(self, request, **kwargs):
        min_date_str = request.POST.get('min_date')
        min_date_str = min_date_str[:24]
        max_date_str = request.POST.get('max_date')
        max_date_str = max_date_str[:24].replace('00:00:00', '23:59:59')

        min_date = datetime.strptime(min_date_str, "%a %b %d %Y %H:%M:%S").replace(tzinfo=local_timezone)
        max_date = datetime.strptime(max_date_str, "%a %b %d %Y %H:%M:%S").replace(tzinfo=local_timezone)

        hashtag = request.POST.get('hashtag').replace('\n', '').replace(' ', '')

        data = self.get_tweets(self.num_tweets, min_date, max_date, hashtag)

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

    def get_tweets(self, how_many, min_date, max_date, hashtag):

        tweets = Tweet.objects.all()
        date_picker_earliest = tweets.order_by('creation_date')[0].creation_date

        if hashtag != 'All':
            needed_tweets = Hashtag.objects.filter(hashtag=hashtag).values('tweet_id')
            tweets = Tweet.objects.filter(tweet_id__in=needed_tweets)

        tweets = tweets.filter(creation_date__gte=min_date)
        tweets = tweets.filter(creation_date__lte=max_date)

        data = [
            tweets.filter(sentiment_string="pos").count(),
            tweets.filter(sentiment_string="neu").count(),
            tweets.filter(sentiment_string="neg").count()
        ]

        recent_tweets = self.get_recent_tweets(tweets.order_by("-creation_date"), how_many)

        rtSorted = list(tweets.order_by("-rt_count").filter(is_rt=False))
        rtSorted = rtSorted[:how_many]
        rtSorted = fixNames(rtSorted)

        favSorted = list(tweets.order_by("-fav_count").filter(is_rt=False))
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

        if (len(tweets) > 0):
            latest = tweets[0].creation_date
            earliest = date_picker_earliest
        else:
            latest = datetime.now()
            earliest = datetime.now()

        tweet_data = {'sentimentCounts': data, 'retweetCounts': rtSorted, 'favouriteCounts': favSorted,
                      'replyCounts': repSorted, 'recentTweets': recent_tweets, 'topRetweet': topRtTweet,
                      'topFavorite': topFavTweet, 'topReply': topReplyTweet, 'tweets': tweets,
                      'min_date': earliest, 'max_date': latest, 'relative_earliest': min_date}
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
