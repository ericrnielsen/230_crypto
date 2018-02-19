import pandas as pd
from tqdm import tqdm
import sys
from datetime import datetime
from datetime import timedelta
from langdetect import detect

# Globals
SUBREDDITS = [  "bitcoin", "ethereum", "litecoin", 
                "btc", "bitcoinmarkets", 
                "cryptocurrency", "cryptomarkets", "altcoin", "cryptocurrencies", "blockchain"]

RAW_FILEPATH = "raw/"
LABELED_FILEPATH = "labeled/"
#ALL_SUB_RAW_FILE = "all_sub_raw.csv"
#ALL_SUB_LABELED_FILE = "all_sub_labeled"
ALL_SUB_RAW_FILE = "score10_all_sub_raw.csv"
ALL_SUB_LABELED_FILE = "score10_all_sub_labeled"

BTC_PRICE_FILE = "../price_data/BTC.csv"
ETH_PRICE_FILE = "../price_data/ETH.csv"
LTC_PRICE_FILE = "../price_data/LTC.csv"

TRAIN = "_train.csv"
DEV = "_dev.csv"
TEST = "_test.csv"

TRAIN_START = '01/01/2017'
TRAIN_END = '12/31/2017'
DEV_START = '01/01/2018'
DEV_END = '02/17/2018'

############################################################################
# Calculate coin price changes (1 day and 2 days out)
############################################################################
def calc_price_changes(coin_df, start_date, stop_date):

    # Will return dict: keys are dates, values represent price change 1 day later and 2 days later
    # (1 means price goes up, 0 means price goes down)
    to_return = {}

    # Loop through price data
    for index, row in coin_df.iterrows():

        # Ignore last 2 dates
        if index == (coin_df.shape[0] - 1) or index == (coin_df.shape[0] - 2):
            continue
        else:

            # Get date into correct format
            date_str = datetime.strptime(row['Date'], '%Y-%m-%d').strftime('%m/%d/%Y')

            # Compute price change
            price_now = row['Close']
            price_one = coin_df.loc[index + 1]['Close']
            price_two = coin_df.loc[index + 2]['Close']
            change_one = 1 if (price_one - price_now) > 0 else 0
            change_two = 1 if (price_two - price_now) > 0 else 0

            # Add to dict
            to_return[date_str] = [change_one, change_two]

    return to_return

############################################################################
# Label news headlines / tweets
############################################################################
def label(subs_df, bitcoin_prices, ethereum_prices, litecoin_prices):

    # Setup
    data = []
    train_end_index, dev_start_index = 0, 0
    first_dev_date = datetime.strptime(DEV_START, '%m/%d/%Y')

    # Reverse order (now earliest to latest)
    subs_df = subs_df.iloc[::-1].reset_index(drop=True)

    # Loop through all posts
    for index, row in subs_df.iterrows():

        # Will store data in temp dict, then append to master list
        temp_dict = {}

        # Grab post info
        date = row['date']
        temp_dict['date'] = date
        temp_dict["subreddit"] = row['subreddit']
        temp_dict["title"] = row['title']
        temp_dict["score"] = row['score']
        temp_dict["num_comments"] = row['num_comments']

        # Get price data for headline date
        try:
            temp_dict['bitcoin_one'] = bitcoin_prices[date][0]
            temp_dict['bitcoin_two'] = bitcoin_prices[date][1]
            temp_dict['ethereum_one'] = ethereum_prices[date][0]
            temp_dict['ethereum_two'] = ethereum_prices[date][1]
            temp_dict['litecoin_one'] = litecoin_prices[date][0]
            temp_dict['litecoin_two'] = litecoin_prices[date][1]
        except:
            continue 

        # Append to master list
        data.append(temp_dict)

        # Grab index of post if applicable
        if train_end_index == 0 and datetime.strptime(date, '%m/%d/%Y') == first_dev_date:
            train_end_index = index -1
            dev_start_index = index

    # Store the list of data in a Pandas dataframe, reverse order
    labeled_df = pd.DataFrame(data)
    labeled_df = labeled_df.reindex(columns=["date", "subreddit", "score", "num_comments", "title", \
                                        "bitcoin_one", "bitcoin_two", \
                                        "ethereum_one", "ethereum_two", \
                                        "litecoin_one", "litecoin_two"])

    # Determine start and stop indices for each dataset
    train_start_index = 0
    dev_end_index = labeled_df.shape[0] - 1

    # Split dataframe
    train = labeled_df[labeled_df.index.isin(range(train_start_index,train_end_index))]
    dev = labeled_df[labeled_df.index.isin(range(dev_start_index,dev_end_index))]

    # Save to csv files
    train.to_csv(LABELED_FILEPATH + ALL_SUB_LABELED_FILE + TRAIN)
    dev.to_csv(LABELED_FILEPATH + ALL_SUB_LABELED_FILE + DEV)

############################################################################
# Main
############################################################################
def main():

    # Define start and stop dates
    start_date = datetime.strptime(TRAIN_START, '%m/%d/%Y')
    stop_date = datetime.strptime(DEV_END, '%m/%d/%Y')

    # Load coin data, compute price changes
    if (True):
        bitcoin_df = pd.read_csv(BTC_PRICE_FILE)
        ethereum_df = pd.read_csv(ETH_PRICE_FILE)
        litecoin_df = pd.read_csv(LTC_PRICE_FILE)
        bitcoin_prices = calc_price_changes(bitcoin_df, start_date, stop_date)
        ethereum_prices = calc_price_changes(ethereum_df, start_date, stop_date)
        litecoin_prices = calc_price_changes(litecoin_df, start_date, stop_date)

    # Label data
    if (True):

        # Load all subreddit post raw data 
        subs_df = pd.read_csv(RAW_FILEPATH + ALL_SUB_RAW_FILE)
        label(subs_df, bitcoin_prices, ethereum_prices, litecoin_prices)


if __name__ == '__main__':
	main()