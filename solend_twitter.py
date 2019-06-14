import numpy as np
import pandas as pd
import re
import twitter_credentials
from textblob import TextBlob
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Cursor
from tweepy import API
import argparse


def authenticate_twitter_app():
    auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,
                        twitter_credentials.CONSUMER_SECRET)
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN,
                          twitter_credentials.ACCESS_TOKEN_SECRET)
    return auth


class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    # def get_usertl_tweets(self, num_tweets=300):
    #     usertl_tweets = []
    #     for tweet in Cursor(self.twitter_client.user_timeline,
    #                         id=self.twitter_user).items(num_tweets):
    #         usertl_tweets.append(tweet)
    #     return usertl_tweets

    def get_user_tweets(self):
        user_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline,
                            id=self.twitter_user).items():
            user_tweets.append(tweet)
        return user_tweets

    def get_favorites(self):
        favorites = []
        for favorite in Cursor(self.twitter_client.favorites,
                               id=self.twitter_user).items():
            favorites.append(favorite)
        return favorites

    def get_user_retweets(self):
        user_retweets = []
        for tweet in Cursor(self.twitter_client.retweets,
                            id=self.twitter_user).items():
            user_retweets.append(tweet)
        return user_retweets


def start_tweet_sentimentation():
    CLIENT = TwitterClient()
    ANALYZER = TweetAnalyzer()
    api = CLIENT.get_twitter_client_api()
    # tweets = api.user_timeline(screen_name=args['username'], count=200)
    valid_user = True if api.get_user(screen_name=args['username'])\
        else False
    if not valid_user:
        msg = "Invalid Username"
        print(msg)
        return msg
    tweets = {
        'user_tweets': CLIENT.get_user_tweets,
        'user_retweets': CLIENT.get_user_retweets,
        'user_favorites': CLIENT.get_favorites,
    }
    frame_data = ANALYZER.tweets_to_df(ANALYZER.analyze_sentiment, tweets)

    return frame_data


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets
    """

    def clean_tweet(self, tweet):
        return ' '.join(re.sub(
                        r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)",
                        " ",
                        tweet).split())

    def analyze_sentiment(self, tweet):
        tweet_sentiment = TextBlob(self.clean_tweet(tweet))

        if tweet_sentiment.sentiment.polarity > 0:
            return 1
        elif tweet_sentiment.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_df(self, analyze, *tweets):
        self.df = pd.DataFrame(data=[tweet.text
                                     for tweet in tweets['user_tweets']],
                               columns=['user_tweets'])
        self.df['UT_sentiment'] = np.array(
            [analyze(tweet) for tweet in self.df['user_tweets']]
                                 )
        self.df['retweets'] = np.array(
            [tweet.text for tweet in tweets['user_retweets']]
                             )
        self.df['RE_sentiment'] = np.array(
            [analyze(tweet) for tweet in self.df['retweets']]
                                 )
        self.df['favorites'] = np.array(
            [tweet.text for tweet in tweets['user_favorite']]
                             )
        self.df['FAV_sentiment'] = np.array(
            [analyze(tweet) for tweet in self.df['favorites']]
                                 )
        return self.df

    def export(self, path):
        self.df.to_csv(path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--username", required=True,
                    help="Twitter username to analyze")
    ap.add_argument("-o", "--output", type=str, default='sentiments.csv')
    args = vars(ap.parse_args())
    start_tweet_sentimentation()