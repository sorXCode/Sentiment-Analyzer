import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
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
    """
    Note: on_data's data is type<string> and not a type<'tweepy.models.ResultSet'>
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
        self.count = 0

    def on_data(self, data):
        if self.count < 3:
            try:
                self.count += 1
                print(type(data))
                with open(self.fetched_tweets_filename, 'a') as twitter_file:
                    json.dump(data, twitter_file, indent=4,
                              separators=(',', ':'))
            except BaseException as e:
                print(f"Error on_data: {str(e)}")
            return True
        else:
            return False

    def on_error(self, status):
        print(status)
        if status == 402:
            # stop on_data method if rate limit reached
            return False


class TweetAnalyzer():
    """
    Functionality for ananlyzing and categorizing content from tweets
    """

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_df(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets],
                          columns=['tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        # print(df)
        return df


if __name__ == "__main__":
    TWITTER_CLIENT = TwitterClient()
    TWEET_ANALYZER = TweetAnalyzer()
    api = TWITTER_CLIENT.get_twitter_client_api()
    tweets = api.user_timeline(screen_name='dopeycutie', count=200)
    # print(type(tweets))
    # # print(TWITTER_CLIENT.get_usertl_tweets(1))

    # with open('_tweets.pkl', 'rb') as tweets_file:
    #     tweets = pickle.loads(tweets_file.read())
    # print(tweets)

    df = TWEET_ANALYZER.tweets_to_df(tweets)
    df['sentiment'] = np.array([TWEET_ANALYZER.analyze_sentiment(tweet)
                                for tweet in df['tweets']])
    # print(df.head(5))
    # MEAN_TWEET_LENGTH = np.mean(df['len'])

    # HASH_TAG_LIST = ['earth', 'love', 'man', ]
    # FETCHED_TWEET_FILENAME = '_tweets.json'
    # TWITTER_CLIENT = TwitterClient('sorXCode')
    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(FETCHED_TWEET_FILENAME, HASH_TAG_LIST)

    # NUMBER_OF_MOST_LIKED_TWEET = np.mean(df['likes'])
    # time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    # time_likes.plot(figsize=(16, 4), color='r', label='Likes', legend=True)
    # time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    # time_retweets.plot(figsize=(16, 4), color='b', label='retweets', legend=True)
    # plt.show()