# Contains the source code

from TwitterAPI import TwitterAPI
import json
import sentimentTest
from TwitterSearch import *
from requests.exceptions import ConnectionError

# Required keys to access the API
consumer_key = 'w645Oz4LizFb9bd1UzbAbdzVq'
consumer_secret = '9UfawqpsphzYHyjKi6S1j06AyLagDn4EvaXZiVFVeU99KtiG7u'
access_token_key = '1113900372-SIKdu4TXMdDEpsBBqdIdurWvjH5Mt1SwDaEhAcz'
access_token_secret = 'YoPJzhZvngJP6KVnW8XZmytU5AH1PZHEJILnb6yYJCLdm'


# Stream all tweets relevant to the hashtags
# hashtags: list containing strings that are the hashtags
def stream(hashtags):
    try:
        tso = TwitterSearchOrder()
        tso.set_keywords(['yegtraffic'])

        # Provides the wrapper with the necessary data for making the calls and retrieving the data
        ts = TwitterSearch(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token_key,
            access_token_secret=access_token_secret
        )

        tweet_id_array = []  # using array instead of calling twitter search again, to make it more time efficient
        count = 0
        for tweet in ts.search_tweets_iterable(tso):
            print tweet['text']
            print
            count += 1

        print count
    except (TwitterSearchException, ConnectionError) as e:  # take care of all those ugly errors if there are some
        print'Exception:', e

    # api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
    #
    # # Loops used for continous stream
    # while True:
    #     # Request the live tweets
    #     r = api.request('statuses/filter', {'track': hashtags})
    #
    #     for item in r.get_iterator():
    #         if 'text' in item:
    #             print item['text'].encode('utf-8')
    #             print 'Sentiment: ' + sentimentTest.sentiment(item['text'])
    #             print '---------------------'
