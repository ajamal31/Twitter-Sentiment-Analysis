#! usr/bin/python3.6

from textblob import TextBlob

while True:
    usr_in = raw_input("Enter a phrase (q to quit): ")
    if usr_in.strip().lower() == "q":
        break
    
    sentiment = TextBlob(usr_in)
    
    if sentiment.polarity > 0 :
        print("That statement is positive (" + str(sentiment.polarity) + ")")
    elif sentiment.polarity < 0:
        print("That statement is negative (" + str(sentiment.polarity) +  ")")
    else:
        print("That statement is neutral (" + str(sentiment.polarity) + ")")