#! usr/bin/python3.6

from nltk.sentiment.vader import SentimentIntensityAnalyzer

#while True:
 #   usr_in = raw_input("Enter a phrase (q to quit): ")
  #  if usr_in.strip().lower() == "q":
   #     break

def sentiment(tweet):
    sid = SentimentIntensityAnalyzer()
    #sentiment = TextBlob(tweet, analyzer=NaiveBayesAnalyzer())
    ss = sid.polarity_scores(tweet)
    if  ss['compound'] > 0.5 :
        return("That statement is positive (" + str(ss) + ")")
    elif ss['compound'] < -0.5:
        return("That statement is negative (" + str(ss) +  ")")
    else:
        return("That statement is neutral (" + str(ss)   + ")")
