#! usr/bin/python3.6

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

#while True:
 #   usr_in = raw_input("Enter a phrase (q to quit): ")
  #  if usr_in.strip().lower() == "q":
   #     break
def sentiment(tweet):
    sentiment = TextBlob(tweet, analyzer=NaiveBayesAnalyzer())
    
    if sentiment.polarity > 0 :
        return("That statement is positive (" + str(sentiment.polarity) + ")")
    elif sentiment.polarity < 0:
        return("That statement is negative (" + str(sentiment.polarity) +  ")")
    else:
        return("That statement is neutral (" + str(sentiment.polarity) + ")")