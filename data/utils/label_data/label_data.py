import pandas as pd
from tqdm import tqdm
import sys
from datetime import datetime
from datetime import timedelta
import numpy as np

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
DEV_START = '01/17/2018'
DEV_END = '02/17/2018'

############################################################################
# Calculate coin price changes (1 day and 2 days out) and use to label
############################################################################
def label(coin_df, start_date, stop_date):

    # Add 2 new columns (+1 day and +2 day labels)
    coin_df['one_day_label'], coin_df['two_day_label'] = 0, 0

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

            # Add to new df
            coin_df.set_value(index, 'one_day_label', change_one)
            coin_df.set_value(index, 'two_day_label', change_two)

    return coin_df

############################################################################
# Add media scores
############################################################################
def add_media_scores(coin_df):

    # Add new column (for media score)
    coin_df['headlines'], coin_df['tweets'], coin_df['reddit'] = 0., 0., 0.

    # Loop through price data
    for index, row in coin_df.iterrows():

        # TEMPORARY - adding random numbers
        score1, score2, score3 = np.random.random(), np.random.random(), np.random.random()
        coin_df.set_value(index, 'headlines', score1)
        coin_df.set_value(index, 'tweets', score2)
        coin_df.set_value(index, 'reddit', score3)

    return coin_df
    
############################################################################
# Main
############################################################################
def main():

    # Define start and stop dates
    start_date = datetime.strptime(TRAIN_START, '%m/%d/%Y')
    stop_date = datetime.strptime(DEV_END, '%m/%d/%Y')

    # Load coin data, compute price changes, and use to label
    if (True):
        bitcoin_df = pd.read_csv(BTC_PRICE_FILE)
        ethereum_df = pd.read_csv(ETH_PRICE_FILE)
        litecoin_df = pd.read_csv(LTC_PRICE_FILE)

        bitcoin_df = label(bitcoin_df, start_date, stop_date)
        ethereum_df = label(ethereum_df, start_date, stop_date)
        litecoin_df = label(litecoin_df, start_date, stop_date)

    # Add media scores
    bitcoin_df = add_media_scores(bitcoin_df)
    ethereum_df = add_media_scores(ethereum_df)
    litecoin_df = add_media_scores(litecoin_df)

    for index, row in bitcoin_df.iterrows():
        print row


if __name__ == '__main__':
	main()