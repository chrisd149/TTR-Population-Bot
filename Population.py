import requests

# this requests the population api, and formats it into the data we need (i.e. the population)
population_api = 'https://www.toontownrewritten.com/api/population'

request = requests.get(url=population_api, params=None)

data = request.json()
population = data['totalPopulation']  # formats data to only include population data
