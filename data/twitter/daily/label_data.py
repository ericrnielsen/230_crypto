'''
This script merges a csv with all tweets and a csv with all dates+labels to produce labeled tweets 
'''

import pandas as pd

labels = pd.read_csv(r'C:\Users\ericr\Google Drive\schoolwork\current classes\CS 230\Project\GetOldTweets-python\twitter_data\labels.csv')
tweets = pd.read_csv(r'C:\Users\ericr\Google Drive\schoolwork\current classes\CS 230\Project\GetOldTweets-python\twitter_data\joined.csv')

labeled_tweets = tweets.merge(labels, on='Date')

labeled_tweets.to_csv(path_or_buf=r'C:\Users\ericr\Google Drive\schoolwork\current classes\CS 230\Project\GetOldTweets-python\twitter_data\labeled_tweets.csv', index=False)
