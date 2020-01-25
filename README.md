# TTR Population Bot

This is a Tweepy bot that posts updated graphics of Toontown's population every hour of every day, every week.  The bot uses the Tweepy module to connect to Twitter, send a HTTP GET request to Toontown Rewritten's [Population API](https://github.com/ToontownRewritten/api-doc/blob/master/population.md) to get the population data, and post the information in a graph every week.  

The current working twitter bot can be found at https://twitter.com/TTR_Population.

![lit](https://user-images.githubusercontent.com/48182689/71801237-4bfe3f00-3028-11ea-8a1f-62b81ae9b2f8.png)

<h2>Installing</h2>
A Keys.py file is need in order to run the bot.  This requires 4 keys from a twitter developer app, which can be obtained after making a Twitter Developer Account at https://developer.twitter.com/en/apply-for-access.
An example Keys.py file would look like this:

```
consumer_key = 'UYSVoHrPfszAksw4y5zpV8YWm'
consumer_secret = 'fynksBZJjasZgaXQ09fbkj98S5KKLVZXcXT95DRzfVh07Y2cTM'
access_key = '1283567691629436596-6ZpLjqNS7zpzjJRwGG6fegHJPXaNHK'
access_secret = 'uLsYd9xpZqYwdfdTuNe5ixtzDqA5rL7EwN4kf6EQFVrHi'
```

<h3>Windows</h3>
Git https://git-scm.com/downloads is needed if you are cloning the repository in the command line. Follow the steps below in the command line. Skip the first line if you downloaded the zip file.

```
git clone https//:github.com/chrisd149/TTR-Population-Bot.git
cd TTR-Population-Bot
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m Bot.py
```

<h3>Linux</h3>
This was tested on Kubuntu 19.10, and should apply to recent distros of Ubuntu and Debian as well.

```
sudo apt-get install git && sudo apt-get install python3-pip
git clone https//:github.com/chrisd149/TTR-Population-Bot.git
cd TTR-Population-Bot
pip3 install -r requirements.txt
python3 -m Bot.py
```

<h3>MacOS</h3>
Support for MacOS is not currently planned as of now.

<h2>Built With</h2>

*	[***Twitter***](https://www.twitter.com) - Platform used to send posts.

*	[***Toontown Rewritten***](https://www.toontownrewritten.com/) - APIs used from to report on ingame data.

*	[***PyCharm***](https://www.jetbrains.com/pycharm/) - IDE used to build program.



<h2>Authors</h2>

Main Author: Christian M Diaz

<h3>Contact Info</h3>

*	GitHub UserName: **@chrisd149**

*	Discord Username: **Miguel149#7640**

*	Twitter: **@miguel_TTR**

* Email: **christianmigueldiaz@gmail.com**
	* Active Hours Weekdays: 3pm - 10pm EST
	* Active Hours Weekend: 9pm - 1am EST (Some of the time im availiable to 3am on the weekends)

<h4>All questions and inquiries must be related to the project in some way, unrelated messages will be ignored</h4>
