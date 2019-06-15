'''
Objective: Sentiment analysis of Tweets from twitter backup.
External Tool: Google Cloud Natural Language Processing Toolkit.
Author: Adeyanju Victor (sorXCode)
'''
import re
from zipfile import ZipFile
import pandas as pd


class TweetsSentiment():
    '''
    TweetsSentiment Class: Extracts tweets from twitter_backup_file
    and perform sentiment analysis on tweet.
    '''

    def __init__(self, zip_archive):
        '''
        Initialize program with twitter_backup_file.zip
        '''
        self.zip_file = zip_archive
        self.tweet_file, self.tweets, self.tweets_text = None, None, None
        self.pattern = None

    def extract_tweet_file(self):
        """
        Extracts tweet.js from twitter back-up archive (zip).
        Usage: extract_tweet_file(zip_archive)
        """
        try:
            self.tweet_file = ZipFile(self.zip_file).extract('tweet.js')
        except FileNotFoundError:
            print('File not Found, Check path')

    def extract_tweets(self):
        '''
        Extract tweets from json file and store as pandas \
        DataFrame Obj. Sentiment analysis of the so extracted \
        tweet is also indicated.
        '''
        # Read file into program as string
        with open(self.tweet_file, 'r') as tmp:
            self.tweets = tmp.read()

        # Compile pattern matching tweet full_text in the tweet.js file
        self.pattern = re.compile(r'\"full_text\"\s?:\s?(.+),\n')

        #'''
        #Pandas Dataframe object created with label tweets to store list of
        #tweets extracted via compiled regular expression pattern.
        #'''
        self.tweets_text = pd.DataFrame(data=self.pattern.findall(self.tweets),
                                        columns=['tweets'], dtype='str')
        return self.tweets_text

    def analyze_tweets(self, tweet="Hello!"):
        '''
        Analyzes tweets using Google's Natural Language Processing
        (Sentiment Analysis) tool.
        '''
        
        return tweet.upper()


if __name__ == "__main__":
    FILE_ = 'temp.zip'
    TWEETS = TweetsSentiment(FILE_)
    TWEETS.extract_tweet_file()
    TWEETS.extract_tweets()
    print(TWEETS.tweets_text)
