'''
Objective: Sentiment analysis of Tweets from twitter backup file.
External Tool: Google Cloud Natural Language Processing Toolkit.
Author: sorXCode
'''
import os
import re
from time import sleep

from datetime import datetime
from sys import argv
from zipfile import ZipFile

import inflect
import pandas as pd
from google.cloud import language
from google.cloud.language import enums, types


class TweetsSentiment:
    '''
    TweetsSentiment Class: Extracts tweets from twitter_backup_file
    and perform sentiment analysis on tweet.
    '''

    def __init__(self, zip_archive):
        '''
        Initialize program with twitter_backup_file.zip
        '''
        self.zip_file = zip_archive
        self.tweet_file, self.tweets, self.tweets_text_activity = None, None, None
        self.pattern = None
        self.inflect = inflect.engine()

    def extract_tweet_file(self):
        """
        Extracts tweet.js from twitter back-up archive (zip).
        """
        try:
            self.tweet_file = ZipFile(self.zip_file).extract('tweet.js')
            # return self.tweet_file
        except FileNotFoundError:
            print('File not Found, Check path or backup file')
            # return 'Invalid path'
        self.extract_tweets()

    def extract_tweets(self):
        '''
        Extract tweets from json file and store as pandas \
        DataFrame Obj. Sentiment analysis of the so extracted \
        tweet is also indicated.
        '''
        print("Extracting tweets...")
        sleep(1)
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
                                                 columns=['Tweets'], dtype='str')
        self.tweets_count = self.tweets_text_activity.shape[0]
        print(f"""Analyzing {self.tweets_count} {self.inflect.plural('tweet', self.tweets_count)}\
            go get a cup of coffee!""")
        sleep(1)
        self.tweets_text_activity['Sentiment'] = self.tweets_text_activity['Tweets'].map(
            self.analyze_tweets)
        self.tweets_text_activity = self.tweets_text_activity.append({
            'Tweets': 'Average',
            'Sentiment': self.tweets_text_activity['Sentiment'].sum()}, ignore_index=True)
        self.export_to_csv()
        # return self.tweets_text_activity

    def export_to_csv(self):
        """
        Method to export tweets and sentiment scores to csv.
        """
        self.path = f"./tweets_sentiments{datetime.now():%Y%m%d%H%M%S}.csv"
        self.tweets_text_activity.to_csv(
            self.path, columns=self.tweets_text_activity.columns)
        print(f"File saved to {self.path}")
        self.cleanup()

    def clean_tweets(self, raw_tweet):
        '''
        Removes special characters from tweets using regex 

        return: string with reduced special characters
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

    def analyze_tweets(self, tweet="Hello!"):
        '''
        Analyzes tweets using Google's AutoML Natural Language (Sentiment Analysis) tool.

        Return: Sentiment score (float)
        '''
        try:    # Instantiates a client
            client = language.LanguageServiceClient()
            # The text to analyze
            document = types.Document(
                content=tweet,
                type=enums.Document.Type.PLAIN_TEXT)

            # Calculates the sentiment of a text
            sentiment = client.analyze_sentiment(
                document=document).document_sentiment
                #add progress bar here
            return sentiment.score
        except Exception as e:
            print(e)
            return 0

    def cleanup(self):
        '''
        Remove tmp files in path
        '''
        os.remove(self.tweet_file)

    def main(self):
        '''
        Program Runner
        '''
        print("Starting...")
        sleep(1)
        self.extract_tweet_file()
        self.analyze_tweets()


if __name__ == "__main__":
    Tweetsentiment = TweetsSentiment(argv[1])
    Tweetsentiment.main()
