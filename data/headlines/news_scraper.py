
'''
Script to scrape cryptocurrency news headlines
'''
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import re

# --- Update the following as needed
NUM_PAGES = 327
#DOMAIN = "https://www.cryptocoinsnews.com/news/page/"
DOMAIN = "https://www.coindesk.com/page/"
#FILE_PATH = "../data/"
FILE_PATH = ""
CSV_NAME = "coindesk_news_headlines.csv"
CSV_NAME_CORRECT = "coindesk_news_headlines_correct.csv"

# ---


def extract_coindesk_main_articles(soup, data):
	results = soup.find_all('div', class_= 'post-info')
	for item in results:
		temp_dict = {}

		# Grab the headline
		headline = item.find("p", class_ = None).text.encode("utf8")
		temp_dict['title'] = headline

		# Grab the time
		timestamp = item.find('time')['datetime']
		date = timestamp.split('T')[0]
		time = timestamp.split('T')[1].split('+')[0]
		temp_dict['date'] = date + ' ' + time

		# Set source
		temp_dict['source'] = 'coindesk1.com'

		# Append to master
		data.append(temp_dict)

	return data

def extract_coindesk_featured_articles(soup, data):
	results = soup.find_all('div', class_= 'article-meta')
	for item in results:
		temp_dict = {}

		# Grab the headline
		headline = item.find("h3").text.encode("utf8")
		temp_dict['title'] = headline

		# Grab the time
		timestamp = item.find('time')['datetime']
		date = timestamp.split('T')[0]
		time = timestamp.split('T')[1].split('+')[0]
		temp_dict['date'] = date + ' ' + time

		# Set source
		temp_dict['source'] = 'coindesk2.com'

		# Append to master
		data.append(temp_dict)

	return data

if (False):
	# Begin loop through all pages and store data
	# Data is stored in a list of dictionaries
	# ex: [ {'title': 'bitcoin up 1000', 'date': 27/09/2017}, ... ]
	data = []
	for num in tqdm(range(1, NUM_PAGES)):
		r = requests.get(DOMAIN + str(num) + "/", headers={'User-Agent': 'Mozilla/5.0'})
		c = r.content
		soup = BeautifulSoup(c, "html.parser")
		#print(soup.prettify())

		# Process the initial 
		try:
			data = extract_coindesk_featured_articles(soup, data)
		except:
			continue

		data = extract_coindesk_main_articles(soup, data)

	# Store the list of data in a 
	results_df = pd.DataFrame(data)
	print("Scraped {} headlines".format(results_df.shape[0]))
	print(results_df.head())

	# Save to csv 
	results_df.to_csv(FILE_PATH + CSV_NAME)

if (True):
	headlines_df = pd.read_csv(FILE_PATH + CSV_NAME)

	# Drop any headlines out of our date range
	headlines_df = headlines_df[pd.to_datetime(headlines_df.date) > pd.to_datetime("2017-01-01 00:00:00")]
	headlines_df = headlines_df[pd.to_datetime(headlines_df.date) < pd.to_datetime("2018-03-07 00:00:00")]
	headlines_df = headlines_df[headlines_df.columns[~headlines_df.columns.str.contains('Unnamed:')]]

	headlines_df.to_csv(FILE_PATH + CSV_NAME_CORRECT)




