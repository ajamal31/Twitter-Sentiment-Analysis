# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from database.models import Tweet
from nltk import word_tokenize

# Create your views here.


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        data = [
            Tweet.objects.filter(sentiment_string="pos").count(),
            Tweet.objects.filter(sentiment_string="neu").count(),
            Tweet.objects.filter(sentiment_string="neg").count()
        ]

        tweets = Tweet.objects.all()
        rtSorted = list(tweets.order_by("-rt_count"))
        rtSorted = rtSorted[:10]

        favSorted = list(tweets.order_by("-fav_count"))
        favSorted = favSorted[:10]
        # d3 cannot create two sperate entries for something with the same name.
        # Could EASILY become a problem down the line.
        usedNames = []
        for item in favSorted:
            if item.user_id.user_name in usedNames:
                item.user_id.user_name = item.user_id.user_name + " "
            usedNames.append(item.user_id.user_name)

        repSorted = list(tweets.order_by("-rep_count"))
        repSorted = repSorted[:10]

        return render(request, 'index.html',
                      {'sentimentCounts': data, 'retweetCounts': rtSorted, 'favouriteCounts': favSorted,
                       'replyCounts': repSorted})


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
