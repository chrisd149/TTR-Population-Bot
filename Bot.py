import tweepy
from Keys import *
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# You must make a Keys.py with the keys in the auth variables
Time = datetime.datetime.now()
current_time = Time.strftime('%H:%M')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

logger.info(F"Starting bot at {current_time}")

headers = headers_dict  # This is from Keys.py, it is a dictionary of the user-agent info and my email

# APIs
population_api = 'https://www.toontownrewritten.com/api/population'
invasions_api = 'https://www.toontownrewritten.com/api/invasions'
silly_meter_api = 'https://www.toontownrewritten.com/api/sillymeter'


def send_population_tweet():
    Time = datetime.datetime.now()
    tweet_current_time = Time.strftime('%I:%M%p')
    request = requests.get(url=population_api, params=None, headers=headers)
    data = request.json()
    population = data['totalPopulation']  # formats data to only include population data
    contents = "The current population of Toontown Rewritten at {} is {} toons."
    tweet_info = contents.format(tweet_current_time, population)
    print(tweet_info)
    #api.update_status(tweet_info)  # Comment this out if you want to spam messages for testing


def follow_followers():
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            logger.info(f"Following {follower.name} at {current_time}")
            follower.follow()


scheduler = BlockingScheduler()
scheduler.add_job(send_population_tweet, 'interval', hours=0.01)  # Sends the automated tweet every 30 minutes
scheduler.add_job(follow_followers, 'interval', hours=0.1)  # Follows back any followers every 6 minutes
scheduler.start()
