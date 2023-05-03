import tweepy
from textblob import TextBlob
import pandas as pd
from tabulate import tabulate
from datetime import datetime, timedelta

API_Key = ""
API_Key_Secret = ""
access_token = ""
Access_Token_Secret = ""

# Authenticate to Twitter
auth = tweepy.OAuthHandler(API_Key, API_Key_Secret)
auth.set_access_token(access_token, Access_Token_Secret)

# Create API object
api = tweepy.API(auth)

# Define search query and date range
search_words = "Python"
since_date = datetime.today() - timedelta(days=7)
until_date = datetime.today()

# Collect tweets using Tweepy Cursor
tweets = tweepy.Cursor(api.search_tweets,
                       q=search_words,
                       lang="en",
                       since_id=None,
                       count=100,
                       tweet_mode='extended').items()

# Create a list to store the tweets and their sentiment
tweet_list = []
for tweet in tweets:
    tweet_date = tweet.created_at
    if since_date <= tweet_date <= until_date:
        tweet_analysis = TextBlob(tweet.full_text)
        if tweet_analysis.sentiment.polarity > 0:
            sentiment = "Positive"
        elif tweet_analysis.sentiment.polarity == 0:
            sentiment = "Neutral"
        else:
            sentiment = "Negative"
        tweet_list.append({'Tweet': tweet.full_text, 'Sentiment': sentiment})

# Create a pandas DataFrame from the tweet list
df = pd.DataFrame(tweet_list)

# Print the DataFrame using tabulate for a nicely formatted table
print(tabulate(df, headers='keys', tablefmt='pretty'))
