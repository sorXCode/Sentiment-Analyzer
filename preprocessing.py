# from nltk.corpus import stopwords
import re
from textblob import TextBlob
import numpy as np


def clean_tweet(tweet):
    # from nltk.tokenize import word_tokenize
    # cleaned = word_tokenize(tweet)
    # cleaned = [word for word in cleaned if word.isalpha() or word.isalnum()]
    # print(tweet)
    tweet = ascii(tweet)
    cleaned = ' '.join(re.sub(
              r"(\w+:\/\/\S+)|(RT)|(\\u\S+)|(#)",
              " ", tweet).split())
    # print(cleaned, end="\n\n")
    cleaned = ' '.join(re.sub(
              r"\\n+",
              '. ', cleaned).split())
#     text = re.search(r'text(.+)source',
#                      cleaned).group(1)
    print(cleaned[1:-2])

# tweet = "\"created_at\":\"Thu Jun 13 11:14:00 +0000 2019\",\"id\":1139128782344916992,\"id_str\":\"1139128782344916992\",\"text\":\"You'll surely fall in love with Ashley's charm and beauty just like how it captured Tan's heart! \\ud83d\\ude0d\\ud83d\\ude0d\\ud83d\\ude0d Check out why\\u2026 https:\\/\\/t.co\\/kUsMJqOkqN\",\"source\":\"\\u003ca href=\\\"https:\\/\\/about.twitter.com\\/products\\/tweetdeck\\\" rel=\\\"nofollow\\\"\\u003eTweetDeck\\u003c\\/a\\u003e\",\"truncated\":true,\"in_reply_to_status_id\":null,\"in_reply_to_status_id_str\":null,\"in_reply_to_user_id\":null,\"in_reply_to_user_id_str\":null,\"in_reply_to_screen_name\":null,\"user\":{\"id\":31313277,\"id_str\":\"31313277\",\"name\":\"ABS-CBN Corporation\",\"screen_name\":\"ABSCBN\",\"location\":\"Manila, Philippines\",\"url\":\"http:\\/\\/www.entertainment.abs-cbn.com\",\"description\":\"The official Twitter account of ABS-CBN, the Philippines' largest network. http:\\/\\/facebook.com\\/ABSCBNnetwork\\/ https:\\/\\/www.instagram.com\\/abscbn\\/\",\"translator_type\":\"none\",\"protected\":false,\"verified\":true,\"followers_count\":996662,\"friends_count\":743,"
# sentiment = TextBlob(clean_tweet(tweet))
# st = sentiment.sentiment.polarity
# print(st)

# text = "it's safe to say that @elonmusk and @TeslaMotors' ambition to \
#         accelerate the advent of sustainable transport is a #success :-)"

# print(TextBlob(text).sentiment.polarity)


d_tweet = "Juventus vs Porto\nBarcelona vs Ajax\nLiverpool vs Man U\nTottenham vs Man City\n\n Nice https://t.co/w71drEEvC9\
        #NairaBetAt10 @TOTALNigeria 27th of June, 1967... If day and month counts \uD83D\uDE09 \
        # RT @officialEFCC: If you feel like you aren't where you ought to be in life, make sure \
        # to keep your hands doing something positive until de… @myzoto issue not resolved!! \
        #  RT @FunnySayings: 5 rules of a relationship:\n\n1. stay faithful\n2. make them feel wanted\n \
        # 3. respect your partner\n4. don't flirt with others… RT @TheFactsBook: 90% of the time it's not \
        #  the person you miss, it's the feelings and moments you had when you were with them."

clean_tweet(d_tweet)
