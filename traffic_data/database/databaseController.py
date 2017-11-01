import database.models as mod
from django.db import models
from django.utils import timezone
from TwitterSearch import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Required keys to access the API
key = 'w645Oz4LizFb9bd1UzbAbdzVq'
secret = '9UfawqpsphzYHyjKi6S1j06AyLagDn4EvaXZiVFVeU99KtiG7u'
token_key = '1113900372-SIKdu4TXMdDEpsBBqdIdurWvjH5Mt1SwDaEhAcz'
token_secret = 'YoPJzhZvngJP6KVnW8XZmytU5AH1PZHEJILnb6yYJCLdm'

# Function responsible for making the api calls and storing the data.


def store(tags):
    try:
        tso = TwitterSearchOrder()
        tso.set_keywords(tags)

        sid = SentimentIntensityAnalyzer()

        # Provides the wrapper with the necessary data for making the calls and retrieving the data
        ts = TwitterSearch(
            consumer_key=key,
            consumer_secret=secret,
            access_token=token_key,
            access_token_secret=token_secret
        )
        count = 0
        for tweet in ts.search_tweets_iterable(tso):
            count += 1
            ss = sid.polarity_scores(tweet['text'])
            u = mod.User(
                tweet['user']['id'],
                tweet['user']['screen_name'],
                tweet['user']['followers_count'],
                tweet['user']['favourites_count'],
                tweet['user']['friends_count'],
                tweet['user']['created_at'],
                timezone.now(),
                tweet['user']['statuses_count']
            )

            mod.User.insert_user(
                tweet['user']['id'],
                tweet['user']['screen_name'],
                tweet['user']['followers_count'],
                tweet['user']['favourites_count'],
                tweet['user']['friends_count'],
                tweet['user']['created_at'],
                tweet['user']['statuses_count']
            )

            mod.Tweet.insert_tweet(
                tweet['id'],
                tweet['text'],
                tweet['created_at'],
                tweet['favorite_count'],
                tweet['retweet_count'],
                tweet['in_reply_to_status_id'],
                tweet['lang'],
                u,
                ss['compound'],
                ss['pos'],
                ss['neg'],
                ss['neu'],
                get_sentiment_string(ss['compound'])
            )
            hashtags_list = tweet['entities']['hashtags']
            # Add the hashtags and duplicates are not added
            for hashtag in hashtags_list:
                if not mod.Hashtag.objects.filter(tweet_id=tweet['user']['id'], hashtag=hashtag['text'].lower()):
                    mod.Hashtag.insert_hashtag(
                        tweet['user']['id'], (hashtag['text'].lower()))

             # Stop after 200 tweets but this will be removed
            if count >= 200:
                break
        print 'tweet count:', count
    except TwitterSearchException as e:  # take care of all those ugly errors if there are some
        print(e)


def get_sentiment_string(compound):
    if (compound >= 0.5):
        return "pos"
    elif (compound <= -0.5):
        return "neg"
    else:
        return "neu"

# I added this for debugging purposes before but this can go if it's not needed


def print_user(tweet):
    print ('id:', tweet['user']['id'], 'screen name:', tweet['user']['screen_name'], 'followers_count:',
           tweet['user']['followers_count'], 'favourites_count:', tweet['user']['favourites_count'], 'friends_count:',
           tweet['user']['friends_count'], 'created_at:', tweet['user']['created_at'], 'statuses_count:',
           tweet['user']['statuses_count'])
    print ''

# These need to be in the controller not here but it's here for testing.


def updateDatabase():
    hashtags = ['yegtraffic']
    print "Getting data and storing it..."
    store(hashtags)
    print("Data stored")
