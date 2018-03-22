import pandas as pd
from tqdm import tqdm
import sys
from datetime import datetime
import datetime as dt
from datetime import timedelta
from langdetect import detect

# Globals
RAW_FILEPATH = ""
LABELED_FILEPATH = "labeled_new/"
#ALL_SUB_RAW_FILE = "all_sub_raw.csv"
#ALL_SUB_LABELED_FILE = "all_sub_labeled"
HEADLINE_RAW_FILE = "coindesk_news_headlines_correct.csv"
HEADLINE_LABELED_FILE = "coindesk_news_headlines_labeled"

BTC_PRICE_FILE = "../price_data/BTC-hourly-pc.csv"
NEW_PRICE_FILE = "../price_data/BTC-hourly-pc-new.csv"

TRAIN = "_train.csv"
DEV = "_dev.csv"
TEST = "_test.csv"

TRAIN_START = '01/01/2017'
TRAIN_END = '02/06/2018'
DEV_START = '02/07/2018'
DEV_END = '03/06/2018'

############################################################################
# Calculate coin price changes
############################################################################
def new_calc_price_changes(coin_df):

    # Drop current price change column
    coin_df = coin_df.drop('Percent Change', 1)

    # Add new columns
    coin_df['1hr Percent Change'] = 0.
    coin_df['2hr Percent Change'] = 0.
    coin_df['6hr Percent Change'] = 0.
    coin_df['12hr Percent Change'] = 0.
    coin_df['24hr Percent Change'] = 0.

    # Loop through price data
    for index, row in coin_df.iterrows():

        # Get current price
        price_now = row['Close']

        # Compute price change +1 hr
        try:
            price_1hr = coin_df.loc[index + 1]['Close']
            change_1hr = ((price_1hr - price_now) / price_now) * 100
        except:
            change_1hr = 0.0

        # Compute price change +2 hr
        try:
            price_2hr = coin_df.loc[index + 2]['Close']
            change_2hr = ((price_2hr - price_now) / price_now) * 100
        except:
            change_2hr = 0.0

        # Compute price change +6 hr
        try:
            price_6hr = coin_df.loc[index + 6]['Close']
            change_6hr = ((price_6hr - price_now) / price_now) * 100
        except:
            change_6hr = 0.0

        # Compute price change +12 hr
        try:
            price_12hr = coin_df.loc[index + 12]['Close']
            change_12hr = ((price_12hr - price_now) / price_now) * 100
        except:
            change_12hr = 0.0            

        # Compute price change +24 hr
        try:
            price_24hr = coin_df.loc[index + 24]['Close']
            change_24hr = ((price_24hr - price_now) / price_now) * 100
        except:
            change_24hr = 0.0    

        #print '[%s] 1hr: %.4f, 2hr: %.4f, 6hr: %.4f, 12hr: %.4f, 24hr: %.4f' % \
        #    (row['Timestamp'], change_1hr, change_2hr, change_6hr, change_12hr, change_24hr)

        # Add to new columns
        coin_df.set_value(index, '1hr Percent Change', change_1hr)
        coin_df.set_value(index, '2hr Percent Change', change_2hr)
        coin_df.set_value(index, '6hr Percent Change', change_6hr)
        coin_df.set_value(index, '12hr Percent Change', change_12hr)
        coin_df.set_value(index, '24hr Percent Change', change_24hr)

    return coin_df

############################################################################
# Label news headlines / tweets
############################################################################
def label(headlines_df, coin_df):

    # Setup
    data = []
    train_end_index, dev_start_index = 0, 0
    first_dev_date = datetime.strptime(DEV_START, '%m/%d/%Y')

    # Reverse order (now earliest to latest)
    headlines_df = headlines_df.iloc[::-1].reset_index(drop=True)

    # Loop through all posts
    for index, row in headlines_df.iterrows():

        # Will store data in temp dict, then append to master list
        temp_dict = {}

        # Grab post datetime, compute top of next hour
        time_string = row['date']
        time = pd.to_datetime(time_string)
        secs_remaining = (60 * 60) - ((time.minute * 60) + time.second)
        top_hour = time + dt.timedelta(seconds=secs_remaining)
        top_hour_string = top_hour.strftime('%Y-%m-%d %H:%M:%S')

        # Grab timestamp
        temp_dict['date'] = time_string

        # Grab headline title
        temp_dict["title"] = row['title'].rstrip('\n')

        # Get correct labels (based on top of next hour)
        try:
            row = coin_df.loc[coin_df['Timestamp'] == top_hour_string]
            temp_dict["1hr_change"] = float(row['1hr Percent Change'])
            temp_dict["2hr_change"] = float(row['2hr Percent Change'])
            temp_dict["6hr_change"] = float(row['6hr Percent Change'])
            temp_dict["12hr_change"] = float(row['12hr Percent Change'])
            temp_dict["24hr_change"] = float(row['24hr Percent Change'])
        except:
            continue 

        # Append to master list
        data.append(temp_dict)

        # Grab index of post if applicable
        if train_end_index == 0 and time > first_dev_date:
            train_end_index = index -1
            dev_start_index = index

    # Store the list of data in a Pandas dataframe, reverse order
    labeled_df = pd.DataFrame(data)
    labeled_df = labeled_df.reindex(columns=["date", "title", \
                                        "1hr_change", "2hr_change", \
                                        "6hr_change", "12hr_change", \
                                        "24hr_change"])

    # Determine start and stop indices for each dataset
    train_start_index = 0
    dev_end_index = labeled_df.shape[0] - 1

    # Split dataframe
    train = labeled_df[labeled_df.index.isin(range(train_start_index,train_end_index))]
    dev = labeled_df[labeled_df.index.isin(range(dev_start_index,dev_end_index))]

    # Save to csv files
    train.to_csv(LABELED_FILEPATH + HEADLINE_LABELED_FILE + TRAIN)
    dev.to_csv(LABELED_FILEPATH + HEADLINE_LABELED_FILE + DEV)

############################################################################
# Main
############################################################################
def main():

    # Edit price file
    if (False):
        bitcoin_df = pd.read_csv(BTC_PRICE_FILE)
        new_bitcoin_df = new_calc_price_changes(bitcoin_df)
        new_bitcoin_df.to_csv(NEW_PRICE_FILE)

    # Label data
    if (True):
        # Load all subreddit post raw data and bitcoin price data
        headlines_df = pd.read_csv(RAW_FILEPATH + HEADLINE_RAW_FILE)
        coin_df = pd.read_csv(NEW_PRICE_FILE)
        label(headlines_df, coin_df)

if __name__ == '__main__':
	main()