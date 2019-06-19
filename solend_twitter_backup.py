'''
Objective: Sentiment analysis of Tweets from twitter backup.
External Tool: Google Cloud Natural Language Processing Toolkit.
Author: Adeyanju Victor (sorXCode)
'''
import re
import os
from zipfile import ZipFile
import pandas as pd
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


class TweetsSentiment():
    '''
    TweetsSentiment Class: Extracts tweets from twitter_backup_file
    and perform sentiment analysis on tweet.

    Return: int
    '''

    def __init__(self, zip_archive):
        # def __init__(self):
        '''
        Initialize program with twitter_backup_file.zip
        '''
        self.zip_file = zip_archive
        self.tweet_file, self.tweets, self.tweets_text_activity = None, None, None
        self.pattern = None
        self.count = 0

    def extract_tweet_file(self):
        """
        Extracts tweet.js from twitter back-up archive (zip).
        Usage: extract_tweet_file(zip_archive)
        """
        try:
            self.tweet_file = ZipFile(self.zip_file).extract('tweet.js')
            return self.tweet_file
        except FileNotFoundError:
            print('File not Found, Check path')
            return 'Invalid path'

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
        self.pattern = re.compile(r'\"full_text\"\s?:\s?\"(.+)\",\n')

        # '''
        # Pandas Dataframe object created with label tweets to store list of
        # tweets extracted via compiled regular expression pattern.
        # '''
        self.tweets = pd.Series(self.pattern.findall(self.tweets))
        self.tweets = self.tweets.map(self.clean_tweets)

        self.tweets_text_activity = pd.DataFrame(data=self.tweets,
                                                 columns=['tweets'], dtype='str')

        self.tweets_text_activity['sentiment'] = self.tweets_text_activity['tweets'].map(
        self.analyze_tweets)
        print(self.tweets_text_activity.head(20))
        print(self.tweets_text_activity.describe())
        self.tweets_text_activity.to_csv(
            './data.csv', columns=self.tweets_text_activity.columns)
        return self.tweets_text_activity

    def clean_tweets(self, raw_tweet):
        '''
        Removes special characters from tweets using regex and returns cleaned tweet
        '''
        # unicode encoding does not support some characters used in tweet,
        # encoding tweets as ascii for compartibility
        raw_tweet = ascii(raw_tweet)
        cleaned_tweet = ' '.join(re.sub(
            r"(\w+:\/\/\S+)|(RT)|(\\u\S+)|(#)",
            " ", raw_tweet).split())
        cleaned_tweet = ' '.join(re.sub(
            r"\\n+",
            '. ', cleaned_tweet).split())
        return cleaned_tweet

    def analyze_tweets(self, text="Hello!"):
        '''
        Analyzes tweets using Google's AutoML Natural Language (Sentiment Analysis) tool.
        '''
        # Imports the Google Cloud client library
        # from google.cloud import language
        # from google.cloud.language import enums
        # from google.cloud.language import types
        # Instantiates a client
        client = language.LanguageServiceClient()
        # key = "AIzaSyDfD78IilMFoQW4TrtIlhcn5lKmA7W_Fmo"
        # The text to analyze
        # text = 'Every saint has a past. Every sinner has a future.'
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        # Detects the sentiment of the text
        sentiment = client.analyze_sentiment(
            document=document).document_sentiment

        print('Text: {}'.format(text))
        print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
        print(f"{sentiment}")
        return sentiment.score

    def cleanup(self):
        '''
        Remove tmp files in path
        '''
        os.rmdir(self.tweet_file)

    def main(self):
        '''
        Program Runner
        '''
        self.extract_tweet_file()
        self.extract_tweets()
        self.analyze_tweets()
        self.cleanup()

if __name__ == "__main__":
    FILE_ = 'temp.zip'
    Tweetsentiment = TweetsSentiment(FILE_)
    Tweetsentiment.main()
