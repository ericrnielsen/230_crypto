# Imports
import pandas as pd
from datetime import datetime
from datetime import date
import requests

# Constants
CRYPTOS = ['BTC', 'ETH', 'LTC']
START_DATE = '2017-01-01'
END_DATE = 'today'

##############################################################
# Connect to CryptoCompare to get coin data
##############################################################
def get_crypto_data(symbol, comparison_symbol, start_date, end_date):
    # Create datetime objects from start and end dates (default end date is today)
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date == 'today':
        today = '%s-%s-%s' % (date.today().year, date.today().month, date.today().day)
        end_date_obj = datetime.strptime(today, '%Y-%m-%d')
    else:
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
    # Calculate day limit (how many days between start and end dates)
    num_days = int((end_date_obj - start_date_obj).days)
    # Make call to CryptoCompare
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), num_days, 1)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.fromtimestamp(d) for d in df.time]
    # Drop time column and volume from column
    df = df.drop('time', 1)
    df = df.drop('volumeto', 1)
    # Remove time from timestamp column
    for index, row in df.iterrows():
        df.set_value(index, 'timestamp', row['timestamp'].date())
    # Rename columns
    df = df.rename(columns={'close': 'Close', 'high': 'High', 'low': 'Low', 'open': 'Open', 
        'volumefrom': 'Volume', 'timestamp': 'Date'})
    # Reorder columns
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    # Set Date column to be index
    df.set_index('Date', inplace=True)
    # Return
    return df

##############################################################
# Main
##############################################################
def main():
    # Loop through each coin
    for crypto in CRYPTOS:
        # Get coin data (Date, Open, High, Low, Close, Volume)
        data_df = get_crypto_data(crypto, 'USD', START_DATE, END_DATE)
        # Save to csv file
        data_df.to_csv('price_data/%s.csv' % (crypto))

if __name__ == '__main__':
	main()