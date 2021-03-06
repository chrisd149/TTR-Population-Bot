import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tweepy
from Keys import *
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import logging
from datetime import datetime, timedelta
import numpy as np
import statistics
from pytz import timezone

# sets the the timezone to western US
western = timezone('America/Los_Angeles')

population_list = []
weekly_population_list = []

headers = {
    'User-Agent': 'TTR Population Tracker(@TTR_Population) (A twitter bot run by @miguel_TTR) GitHub repository: '
                  'https://github.com/chrisd149/Toontown-Rewritten-API-Bot',
    'From': 'christianmigueldiaz@gmail.com',
    'Accept-Language': 'en-us,',
    'Server': 'TTR Population Tracker Bot'
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# APIs
population_api = 'https://www.toontownrewritten.com/api/population'

scheduler = BlockingScheduler()


class Bot:
    def __init__(self):
        global population_list
        self.get_population()
        self.run_scheduler()

    def get_population(self):
        request = requests.get(url=population_api, params=None, headers=headers)
        data = request.json()
        self.population = data['totalPopulation']  # formats data to only include population data

        population_list.append(self.population)
        weekly_population_list.append(self.population)
        print(population_list)
        print(len(weekly_population_list))

    @staticmethod
    def send_week_population_tweet():
        global weekly_population_list
        contents = f"Weekly Post | {current_day} | @Toontown Rewritten had an average population of {round(statistics.mean(weekly_population_list))} " \
            f"toons, with a peak of {max(weekly_population_list)} toons and a minimum of {min(weekly_population_list)} " \
            f"toons through last week. All times PST. \n #toontown #ttr #toontownrewritten"
        # load image
        image = f'Plot {current_day} week.png'  # finds the graph we saved

        api.update_with_media(image, contents)  # posts the tweet :)
        f = open('data.txt', 'a+')
        f.write(f'{current_day} : {population_list}')
        print('Sent weekly tweet!')
        print(contents)
        weekly_population_list = []
        plt.close()

    def run_scheduler(self):
        scheduler.add_job(self.get_population, 'interval', hours=1.000025)  # Sends HTTP GET request to API
        scheduler.add_job(self.if_day, 'interval', hours=0.0001)  # Checks if the day has changed

    @staticmethod
    def daily_plotter():
        global population_list, weekly_population_list
        if len(population_list) < 24:
            logger.info('Not enough data to plot.')
            population_list = []
            weekly_population_list = []
            get_time()
            # resets all data if started too early
        if len(population_list) > 24:
            logger.info('Too much data to plot.')
            population_list = []
            get_time()
        if len(population_list) == 24:
            # Prepare the data
            y = np.array(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
                          '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'])
            x = population_list
            plt.title(
                f'Hourly population of Toontown every day of week {start_of_week.date().strftime("%m-%d")} - {end_of_week.date().strftime("%m-%d")}')
            plt.ylabel('Population of Toons online')
            plt.xlabel('Hour of Day (PST)')
            
            # Plot the data
            plt.plot(y, x, label=f'{current_day}')
            plt.draw()
            get_time()
            print(weekly_population_list)
            logger.info(f'Plotted data at {current_day}:{current_time}')
            population_list = []

    def weekly_plotter_save(self):
        plt.legend(loc='lower right', fontsize = 'x-small', frameon=False)
        plt.savefig(f'Plot {current_day} week.png', dpi=250)
        logger.info(F"Drew weekly graph at {current_time}, {current_day}")
        plt.close()
        self.send_week_population_tweet()

    def if_day(self):
        global population_list, western
        if startTime.astimezone(western).date() != datetime.today().astimezone(western).date():
            api.update_profile(
                description=f"A bot created by @miguel_TTR. I post a graph of @Toontown Rewritten's population every "
                f"hour every day. Bot is online as of {datetime.today().astimezone(western).strftime('%b, %d')}, "
                f"{Time.astimezone(western).strftime('%I:%M:%S%p')} PST"
            )
            print(f'It is now {datetime.today().astimezone(western).date()}')
            self.daily_plotter()
            self.if_week()

    def if_week(self):
        if start_of_week.date() == datetime.today().astimezone(western).date():
            self.weekly_plotter_save()
            f = open('data.txt', 'a+')
            f.write(f'\nPopulation of Toontown through the week of {start_of_week.date()} - {end_of_week.date()}:')


def get_time():
    global Time, current_day, current_time, date_str, date_obj, start_of_week, end_of_week, startTime
    Time = datetime.now(western)
    startTime = datetime.today().astimezone(western)
    date_str = str(datetime.today().astimezone(western).date())
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').astimezone(western)
    start_of_week = date_obj - timedelta(days=date_obj.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    current_time = Time.strftime('%H:%M:%S')
    current_day = Time.strftime('%A, %B %d')


get_time()
logger.info(F"Starting bot at {current_time}, {current_day}")

Bot()
api.update_profile(
                description=f"A bot created by @miguel_TTR. I post a graph of @Toontown Rewritten's population every "
                f"hour every day. Bot is online as of {datetime.today().astimezone(western).strftime('%b, %d')}, "
                f"{Time.astimezone(western).strftime('%I:%M:%S%p')} PST"
            )
scheduler.start()
