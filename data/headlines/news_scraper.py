
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
NUM_PAGES = 290
#DOMAIN = "https://www.cryptocoinsnews.com/news/page/"
DOMAIN = "https://www.coindesk.com/page/"
FILE_PATH = "../data/"
CSV_NAME = "coindesk_news_headlines.csv"
# ---


def extract_coindesk_main_articles(soup, data):
	results = soup.find_all('div', class_= 'post-info')
	for item in results:
		temp_dict = {}

		# Get the main text
		body_text = item.find("p", class_ = None).text
		temp_dict['headline'] = body_text

		time = item.find('time')
		temp_dict['postdate'] = time['datetime']
		temp_dict['source'] = 'coindesk.com'
		data.append(temp_dict)

	return data

def extract_coindesk_featured_articles(soup, data):
	results = soup.find_all('div', class_= 'article-meta')
	for item in results:
		temp_dict = {}

		# Get the main text
		temp_dict['headline'] = item.find("h3").text

		time = item.find('time')
		temp_dict['postdate'] = time['datetime']
		temp_dict['source'] = 'coindesk.com'
		data.append(temp_dict)

	return data

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






