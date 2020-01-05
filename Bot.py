import tweepy
from Keys import *
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import requests

# You must make a Keys.py with the keys in the auth variables
Time = datetime.datetime.now()
current_time = Time.strftime('%H:%M')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)
print(current_time, 'Starting bot...')

headers = headers_dict  # This is from Keys.py, it is a dictionary of the user-agent info and email

# APIs
population_api = 'https://www.toontownrewritten.com/api/population'
invasions_api = 'https://www.toontownrewritten.com/api/invasions'
silly_meter_api = 'https://www.toontownrewritten.com/api/sillymeter'


def send_population_tweet():
    Time = datetime.datetime.now()
    tweet_current_time = Time.strftime('%I:%M%p')
    pop_request = requests.get(url=population_api, params=None, headers=headers)
    pop_data = pop_request.json()
    population = pop_data['totalPopulation']  # formats data to only include population data
    pop_contents = "The current population of Toontown Rewritten at {} is {} toons."
    pop_tweet_info = pop_contents.format(tweet_current_time, population)
    print(pop_tweet_info)
    api.update_status(pop_tweet_info)


scheduler = BlockingScheduler()
scheduler.add_job(send_population_tweet, 'interval', hours=0.5)
scheduler.start()
