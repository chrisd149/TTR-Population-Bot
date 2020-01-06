import tweepy
from Keys import *
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import statistics

startTime = datetime.today()

population_list = [1605, 1240, 903, 660, 432, 337, 334, 292, 354, 442, 534, 717, 937, 1015, 1166, 1359, 1475, 1579]

headers = {
    'User-Agent': 'TTR Population Tracker(@TTR_Population) (A twitter bot run by @miguel_TTR) GitHub repository: '
                  'https://github.com/chrisd149/Toontown-Rewritten-API-Bot',
    'From': 'christianmigueldiaz@gmail.com'
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# You must make a Keys.py with the keys in the auth variables
Time = datetime.now()
current_time = Time.strftime('%H:%M')
current_day = Time.strftime('%A, %B %d')
print(current_day)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

logger.info(F"Starting bot at {current_time}, {current_day}")

# APIs
population_api = 'https://www.toontownrewritten.com/api/population'
scheduler = BlockingScheduler()


class Bot:
    def __init__(self):
        global population_list
        self.get_population()
        self.run_scheduler()
        self.tweet_current_time = None

    def get_population(self):
        Time = datetime.now()
        self.tweet_current_time = Time.strftime('%I:%M%p')
        request = requests.get(url=population_api, params=None, headers=headers)
        data = request.json()
        self.population = data['totalPopulation']  # formats data to only include population data

        population_list.append(self.population)
        print(population_list)
        print(len(population_list))

    @staticmethod
    def send_population_tweet():
        global startTime
        contents = f"{current_day} | @Toontown Rewritten had an average population of {round(statistics.mean(population_list))} " \
            f"toons, with a peak of {max(population_list)} toons and a minimum of {min(population_list)} toons."
        # load image
        image = f'Plot {current_day}.png'  # finds the graph we saved

        api.update_with_media(image, contents)  # posts the tweet :)
        startTime = datetime.today()

    @staticmethod
    def follow_followers():
        for follower in tweepy.Cursor(api.followers).items():
            if not follower.following:
                logger.info(f"Following {follower.name} at {current_time}")
                follower.follow()

    def run_scheduler(self):
        scheduler.add_job(self.send_population_tweet, 'interval', hours=24)  # Sends the automated tweet every day
        scheduler.add_job(self.get_population, 'interval', hours=1.0005)  # Sends HTTP GET request to API
        scheduler.add_job(self.follow_followers, 'interval', hours=0.1)  # Follows back any followers every 6 minutes
        scheduler.add_job(if_day, 'interval', hours=0.0005)  # Checks if the day has changed


def daily_grapher():
    # Prepare the data
    y = np.array(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
                  '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'])
    x = population_list
    plt.title(f'Population of Toontown every hour on {current_day}')
    plt.ylabel('Population of Toons online')
    plt.xlabel('Time (Eastern Daylight (GMT-5))')
    # Plot the data
    plt.plot(y, x)

    plt.draw()
    plt.savefig(f'Plot {current_day}.png', dpi=150)
    logger.info(F"Drew daily graph at {current_time}, {current_day}")


def if_day():
    global startTime
    global population_list
    if startTime.date() != datetime.today().date():
        print(f'It is now {datetime.today().date()}')
        daily_grapher()
        population_list = []
    else:
        return


Bot()
scheduler.start()

