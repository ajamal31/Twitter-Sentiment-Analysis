# Contains the source code

from TwitterAPI import TwitterAPI

# Required keys to access the API
consumer_key = 'w645Oz4LizFb9bd1UzbAbdzVq'
consumer_secret = '9UfawqpsphzYHyjKi6S1j06AyLagDn4EvaXZiVFVeU99KtiG7u'
access_token_key = '1113900372-SIKdu4TXMdDEpsBBqdIdurWvjH5Mt1SwDaEhAcz'
access_token_secret = 'YoPJzhZvngJP6KVnW8XZmytU5AH1PZHEJILnb6yYJCLdm'

# Stream all tweets relevant to the hashtags
# hashtags: list containing strings that are the hashtags
def stream(hashtags):
    
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)   
    
    # Loops used for continous stream
    while True:
        # Request the live tweets
        r = api.request('statuses/filter', {'track': hashtags})  
        for item in r.get_iterator():
            if 'text' in item:
                print item['text']
            