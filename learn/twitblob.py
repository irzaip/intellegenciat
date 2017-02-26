import tweepy
from textblob import TextBlob

# Step 1 - Authenticate
consumer_key= 'o5aYQk4FyegElpNt3XlxUf5RP'
consumer_secret= '2A388e5WtBwWZf7bmN6IY5ivOgOhigEKrFwnzZhQUXSDnYCQVq'

access_token='39393977-IRS5mr90vPNtQCBX28CYOf5A0K2gzcLDj5z2cLrN3'
access_token_secret='VHCpwcvL1fbqRi0dZvRjLEj29mA9zwdAZTpGPkHTx0m4K'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Step 3 - Retrieve Tweets
public_tweets = api.search('Rizieq')



#CHALLENGE - Instead of printing out each tweet, save each Tweet to a CSV file
#and label each one as either 'positive' or 'negative', depending on the sentiment 
#You can decide the sentiment polarity threshold yourself


for tweet in public_tweets:
    print(tweet.text)
    
    #Step 4 Perform Sentiment Analysis on Tweets
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)
    print("")