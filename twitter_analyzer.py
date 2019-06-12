import numpy as np
import pandas as pd
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy import Cursor
from tweepy import API
import twitter_credentials


class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_usertl_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline,
                            id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friends_list(self, num_friends):
        friends = []
        for friend in Cursor(self.twitter_client.friends,
                             id=self.twitter_user).items(num_friends):
            friends.append(friend)
        return friends

    def get_hometl_tweets(self, num_tweets):
        hometl_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline,
                            id=self.twitter_user).items(num_tweets):
            hometl_tweets.append(tweet)
        return hometl_tweets


# class TwitterAuthentication():
#      """
#      Authenticator
#      """

#     def authenticate_twitter_app(self):
#         auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,
#                             twitter_credentials.CONSUMER_SECRET)
#         auth.set_access_token(twitter_credentials.ACCESS_TOKEN,
#                               twitter_credentials.ACCESS_TOKEN_SECRET)
#         return auth

def authenticate_twitter_app():
    auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,
                        twitter_credentials.CONSUMER_SECRET)
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN,
                          twitter_credentials.ACCESS_TOKEN_SECRET)
    return auth


class TwitterStreamer():
    """
    Streams and process live tweets
    """

    def __init__(self):
        self.twitter_athenticator = authenticate_twitter_app()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        """
        Handles Twitter authentication and the connection to the Twitter\
            Streaming API
        """
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_athenticator
        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list)


class TwitterListener(StreamListener):

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
        except BaseException as e:
            print(f"Error on_data: {str(e)}")
        return True

    def on_error(self, status):
        if status == 402:
            # stop on_data method if rate limit reached
            return False
        print(status)


class TweetAnalyzer():
    """
    Functionality for ananlyzing and categorizing content from tweets
    """
    def tweets_to_df(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets],
                          columns=['Tweets'])
        return df


if __name__ == "__main__":
    TWITTER_CLIENT = TwitterClient()
    TWEET_ANALYZER = TweetAnalyzer()

    api = TWITTER_CLIENT.get_twitter_client_api()
    tweets = api.user_timeline(screen_name='sorXCode', count=20)

    df = TWEET_ANALYZER.tweets_to_df(tweets)

    print(df.head(5))

    # HASH_TAG_LIST = ['Bincom']
    # FETCHED_TWEET_FILENAME = 'tweets.json'

    # TWITTER_CLIENT = TwitterClient('sorXCode')
    # print(TWITTER_CLIENT.get_usertl_tweets(1))
    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweet_filename, hash_tag_list)
