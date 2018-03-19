import pandas as pd

labels = pd.read_csv(r'C:\Users\ericr\Google Drive\schoolwork\current classes\CS 230\Project\GetOldTweets-python\Bitcoin devs\New folder\labels.csv')
tweets = pd.read_csv(r'C:\Users\ericr\Google Drive\schoolwork\current classes\CS 230\Project\GetOldTweets-python\Bitcoin devs\New folder\joined.csv')

labeled_tweets = tweets.merge(labels, on='date')

labeled_tweets.to_csv(path_or_buf=r'C:\Users\ericr\Google Drive\schoolwork\current classes\CS 230\Project\GetOldTweets-python\Bitcoin devs\New folder\labeled_tweets.csv', index=False)