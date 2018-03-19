import glob
import os
import pandas as pd

path = r'C:\Users\ericr\Google Drive\schoolwork\current classes\CS 230\Project\GetOldTweets-python\Bitcoin devs'
all_files = glob.glob(os.path.join(path, "*.csv"))
df_from_each_file = (pd.read_csv(f, sep=';', error_bad_lines=False) for f in all_files)
concatenated_df = pd.concat(df_from_each_file, ignore_index=True)
#concatenated_df = concatenated_df[concatenated_df['retweets'] + concatenated_df['favorites'] > 0] 
concatenated_df.drop(['username', 'retweets', 'favorites', 'geo', 'mentions', 'hashtags', 'id', 'permalink'], 1, inplace=True)
#concatenated_df.to_csv(path_or_buf=r'C:\Users\ericr\Google Drive\schoolwork\current classes\CS 230\Project\GetOldTweets-python\Bitcoin devs\New folder\joined.csv', index=False)
concatenated_df.to_csv(path_or_buf=r'C:\Users\ericr\Google Drive\schoolwork\current classes\CS 230\Project\GetOldTweets-python\Bitcoin devs\New folder\joined.csv')