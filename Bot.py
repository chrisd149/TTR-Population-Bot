import tweepy
from Keys import *
import datetime
from Population import *
import time

# You must make a Keys.py with the keys in the auth variables
Time = datetime.datetime.now()
current_time = Time.strftime('%H:%M')
tweet_current_time = Time.strftime('%I:%M%p')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
print(current_time, 'Starting bot...')


def send_population():
    pop_contents = "The current population of Toontown Rewritten at {} is {} toons."
    pop_tweet_info = pop_contents.format(tweet_current_time, population)
    print(pop_tweet_info)
    api.update_status(pop_tweet_info)
    time.sleep(1800)


while True:
    send_population()

