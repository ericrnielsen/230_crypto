import pandas as pd

labels = pd.read_csv(r'C:\Users\ericr\Google Drive\schoolwork\current classes\CS 230\Project\GetOldTweets-python\twitter_data\labels2.csv')
tweets = pd.read_csv(r'C:\Users\ericr\Google Drive\schoolwork\current classes\CS 230\Project\GetOldTweets-python\twitter_data\joined2.csv')

labeled_tweets = tweets.merge(labels, on='Timestamp')

labeled_tweets.to_csv(path_or_buf=r'C:\Users\ericr\Google Drive\schoolwork\current classes\CS 230\Project\GetOldTweets-python\twitter_data\labeled_tweets2.csv', index=False)
