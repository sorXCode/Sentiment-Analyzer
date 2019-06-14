from nltk.corpus import stopwords
import re
from textblob import TextBlob


def clean_tweet(tweet):
    cleaned = ' '.join(re.sub(
              r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)",
              " ", tweet).split())
    text = re.search(r'text(.+)source',
                     cleaned).group(1)
    print(text)
    return text


# tweet = "\"created_at\":\"Thu Jun 13 11:14:00 +0000 2019\",\"id\":1139128782344916992,\"id_str\":\"1139128782344916992\",\"text\":\"You'll surely fall in love with Ashley's charm and beauty just like how it captured Tan's heart! \\ud83d\\ude0d\\ud83d\\ude0d\\ud83d\\ude0d Check out why\\u2026 https:\\/\\/t.co\\/kUsMJqOkqN\",\"source\":\"\\u003ca href=\\\"https:\\/\\/about.twitter.com\\/products\\/tweetdeck\\\" rel=\\\"nofollow\\\"\\u003eTweetDeck\\u003c\\/a\\u003e\",\"truncated\":true,\"in_reply_to_status_id\":null,\"in_reply_to_status_id_str\":null,\"in_reply_to_user_id\":null,\"in_reply_to_user_id_str\":null,\"in_reply_to_screen_name\":null,\"user\":{\"id\":31313277,\"id_str\":\"31313277\",\"name\":\"ABS-CBN Corporation\",\"screen_name\":\"ABSCBN\",\"location\":\"Manila, Philippines\",\"url\":\"http:\\/\\/www.entertainment.abs-cbn.com\",\"description\":\"The official Twitter account of ABS-CBN, the Philippines' largest network. http:\\/\\/facebook.com\\/ABSCBNnetwork\\/ https:\\/\\/www.instagram.com\\/abscbn\\/\",\"translator_type\":\"none\",\"protected\":false,\"verified\":true,\"followers_count\":996662,\"friends_count\":743,"
# sentiment = TextBlob(clean_tweet(tweet))
# st = sentiment.sentiment.polarity
# print(st)

text = "it's safe to say that @elonmusk and @TeslaMotors' ambition to \
        accelerate the advent of sustainable transport is successful :-)"

print(TextBlob(text).sentiment.polarity)