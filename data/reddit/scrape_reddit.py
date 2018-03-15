import praw
import pandas as pd
from datetime import datetime
from datetime import date
import time

START_DATE = '2017-01-01'
END_DATE = 'today'
SUBREDDITS = [  "bitcoin", "ethereum", "litecoin", 
                "btc", "bitcoinmarkets", 
                "cryptocurrency", "cryptomarkets", "altcoin", "cryptocurrencies", "blockchain"]

RAW_FILEPATH = "raw/"
ALL_SUB_RAW_FILE = "all_sub_raw.csv"

############################################################################
# Convert strings to unix dates
############################################################################
def get_unix_dates(start_date, end_date):

    # Create date objects from start and end dates
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date == 'today':
        today = '%s-%s-%s' % (date.today().year, date.today().month, date.today().day)
        end_date_obj = datetime.strptime(today, '%Y-%m-%d').date()
    else:
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Convert to unix dates and return
    return time.mktime(start_date_obj.timetuple()), time.mktime(end_date_obj.timetuple())

############################################################################
# Scrape single subreddit and save to csv file
############################################################################
def scrape_subreddit(reddit, sub_name, start, end):

    # Just for printing
    print "Starting r.%s" % sub_name.upper()

    # Will be list of dictionaries with post info
    data = []

    # Get all posts for subreddit within desired timeframe
    subreddit = reddit.subreddit(sub_name)
    posts = subreddit.submissions(start, end)

    # Loop through all posts
    i, j = 0, 0
    for post in posts:
        i += 1

        # Get post date, title, score, and num comments; append to master data list
        temp_dict = {}
        temp_dict["date"] = datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')
        temp_dict["title"] = post.title.encode("utf8")
        temp_dict["score"] = post.score
        temp_dict["num_comments"] = post.num_comments
        data.append(temp_dict)

        # Just for printing
        if i == 1 or datetime.fromtimestamp(post.created).date() < current_date.date():
            current_date = datetime.fromtimestamp(post.created)
            print "[%s] Added: %d  Total: %d" % (current_date.strftime('%m/%d/%Y'), (i-j), i)
            j = i

    # Just for printing
    print "Retrieved %d posts from r.%s" % (i, sub_name.upper())

    # Store the list of data in a Pandas dataframe, save to csv
    sub_df = pd.DataFrame(data)
    sub_df.to_csv(RAW_FILEPATH + sub_name + "_sub_raw.csv")

    # Return df
    return sub_df

############################################################################
# Combine all posts into single csv file
############################################################################
def combine_subreddits(frames, min_score, min_comments):

    # If needing to read in all raw data from files
    if not frames:
        frames = []
        for sub_name in SUBREDDITS:
            sub_df = pd.read_csv(RAW_FILEPATH + sub_name + "_sub_raw.csv")
            print "[%s] %d" % (sub_name, sub_df.shape[0])
            sub_df['subreddit'] = sub_name
            frames.append(sub_df)

    # Combine into single df
    subs_df = pd.concat(frames, ignore_index=True)

    # If using thresholds to reduce dataset size
    filename_begin = RAW_FILEPATH
    if min_score:
        subs_df = subs_df[subs_df['score'] >= min_score]
        filename_begin += 'score' + str(min_score) + '_'
    if min_comments:
        subs_df = subs_df[subs_df['num_comments'] >= min_comments]
        filename_begin += 'comments' + str(min_comments) + '_'

    # Sort values in df by descending date
    subs_df['date'] = pd.to_datetime(subs_df['date'])   # Convert date column to datetime objs
    subs_df = subs_df.sort_values(['date'], ascending=[False])           # Sort by descending date
    subs_df['date'] = subs_df['date'].strftime('%Y-%m-%d %H:%M:%S')   # Convert dates back to strings
    subs_df.reset_index(drop=True)                      # Re-index

    # Save all posts to a single raw file
    print "Total posts: %s" % subs_df.shape[0]
    subs_df = subs_df.reindex(columns=["date", "subreddit", "score", "num_comments", "title"])
    subs_df.to_csv(filename_begin + ALL_SUB_RAW_FILE)

############################################################################
# Check what setting different score and num_comments thresholds do to dataset size
############################################################################
def check_thresholds():

    frames = []
    for sub_name in SUBREDDITS:
        sub_df = pd.read_csv(RAW_FILEPATH + sub_name + "_sub_raw.csv")
        sub_df['subreddit'] = sub_name
        frames.append(sub_df)
    subs_df = pd.concat(frames, ignore_index=True)

    # Using different score thresholds
    for min_score in [0, 1, 5, 10, 15, 20, 50, 100]:
        new_df = subs_df[subs_df['score'] >= min_score]
        print "[Min Score: %d] Total posts: %s" % (min_score, new_df.shape[0])

    # Using different num_comments thresholds
    print ""
    for min_comment in [0, 1, 5, 10, 15, 20, 50, 100]:
        new_df = subs_df[subs_df['num_comments'] >= min_comment]
        print "[Min Num Comments: %d] Total posts: %s" % (min_comment, new_df.shape[0])

############################################################################
# Main
############################################################################
def main():

    #################################
    # NORMAL
    #################################
    if (False):

        # Get start and stop unix dates (required by praw)
        start_unix, end_unix = get_unix_dates(START_DATE, END_DATE)

        # Initialize reddit instance
        reddit = praw.Reddit('bot1')

        # Loop through all subreddits
        frames = []
        for sub_name in SUBREDDITS:  
            sub_df = scrape_subreddit(reddit, sub_name, start_unix, end_unix)
            frames.append(sub_df)

        # Combine into single raw datafile
        combine_subreddits(frames, in_score=10, min_comments=None)

    #################################
    # JUST TO COMBINE DATA
    #################################
    if (False):
        combine_subreddits(None, min_score=10, min_comments=None)

    #################################
    # TESTING DIFFERENT THRESHOLDS
    #################################
    if (False):
        check_thresholds()

    #################################
    # SAVING ONLY HEADLINES
    #################################
    if (True):
        subs_df = pd.read_csv(RAW_FILEPATH + "score10_all_sub_raw.csv")
        titles = subs_df['title']
        titles.to_csv(RAW_FILEPATH + "reddit_all_titles.csv")

if __name__ == '__main__':
	main()