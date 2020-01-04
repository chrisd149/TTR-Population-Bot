import tweepy
from Keys import *
import datetime
from Population import *
import time

# You must make a Keys.py with the keys in the auth variables
Time = datetime.datetime.now()
current_time = Time.strftime('%H:%M')
tweet_current_time = Time.strftime('%I%p')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
print(current_time, 'Starting bot...')


def send_population():
    contents = "The current population of Toontown Rewritten at {} is {} toons."
    tweet_info = contents.format(tweet_current_time, population)
    print(tweet_info)
    api.update_status(tweet_info)


if __name__ == "__main__":
    send_population()
    time.sleep(3600)

