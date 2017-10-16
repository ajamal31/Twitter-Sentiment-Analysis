from TwitterAPI import TwitterAPI, TwitterRestPager
from TwitterSearch import *
from database.models import Tweet, User, Hashtag
import json

# Required keys to access the API
key = 'w645Oz4LizFb9bd1UzbAbdzVq'
secret = '9UfawqpsphzYHyjKi6S1j06AyLagDn4EvaXZiVFVeU99KtiG7u'
token_key = '1113900372-SIKdu4TXMdDEpsBBqdIdurWvjH5Mt1SwDaEhAcz'
token_secret = 'YoPJzhZvngJP6KVnW8XZmytU5AH1PZHEJILnb6yYJCLdm'

# Stream all tweets relevant to the hashtags
# hashtags: list containing strings that are the hashtags
def stream(hashtags):
    try:
        tso = TwitterSearchOrder()
        tso.set_keywords(hashtags)

        ts = TwitterSearch(
                consumer_key = key,
                consumer_secret = secret,
                access_token = token_key,
                access_token_secret = token_secret
            )
        count = 0;
        for tweet in ts.search_tweets_iterable(tso):
            Tweet.insert_tweet(tweet['id'])
            #print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))
            print json.dumps(tweet,sort_keys=True, indent=3, separators=(',', ': '))
            break
        print count
    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)
