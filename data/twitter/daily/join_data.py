'''
This script takes output from get_tweets.py and joins everything into a single csv file.
It then filters it based on retweets/favorites and gets rid of unnecessary columns.
'''

import glob
import os
import pandas as pd

path = r'C:\Users\ericr\Google Drive\schoolwork\current classes\CS 230\Project\GetOldTweets-python\twitter_data'
all_files = glob.glob(os.path.join(path, "*.csv"))
df_from_each_file = (pd.read_csv(f, sep=';', error_bad_lines=False) for f in all_files)
concatenated_df = pd.concat(df_from_each_file, ignore_index=True)
concatenated_df = concatenated_df[concatenated_df['retweets'] + concatenated_df['favorites'] > 0] 
concatenated_df.drop(['username', 'retweets', 'favorites', 'geo', 'mentions', 'hashtags', 'id', 'permalink'], 1, inplace=True)

concatenated_df.to_csv(path_or_buf=r'C:\Users\ericr\Google Drive\schoolwork\current classes\CS 230\Project\GetOldTweets-python\twitter_data\tweets.csv', index=False)
