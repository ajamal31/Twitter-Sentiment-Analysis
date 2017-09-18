# Main program

from twython import Twython
from twython import TwythonStreamer
from TwitterAPI import TwitterAPI

consumer_key = 'w645Oz4LizFb9bd1UzbAbdzVq'
consumer_secret = '9UfawqpsphzYHyjKi6S1j06AyLagDn4EvaXZiVFVeU99KtiG7u'
access_token_key = '1113900372-SIKdu4TXMdDEpsBBqdIdurWvjH5Mt1SwDaEhAcz'
access_token_secret = 'YoPJzhZvngJP6KVnW8XZmytU5AH1PZHEJILnb6yYJCLdm'

api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

def main():
    r = api.request('statuses/filter', {'track':'yegtraffic', 'track':'ABRoads', 'track':'edmonton', 'track':'pizza'})
    for item in r.get_iterator():
        if 'text' in item:
            print item['text']
        
main()

