'''
This script must be run from same directory as https://github.com/Jefferson-Henrique/GetOldTweets-python since it runs Exporter.py
It will create an individual output file for each coin for each day 
....had to do this to get same amt of data for each coin each day w/o changing GOT code
....there is probably a way to do it without creating so many csv files...
join_data.py is then used to join all individual files and the filter them and get rid of unnecessary columns
'''

import subprocess
import datetime

base = datetime.datetime.today()
date_list = [str(base - datetime.timedelta(days=x)).split()[0] for x in range(414, 3, -1)] ##[2017-01-01 ... 2018-02-15]
coins = ['Bitcoin', 'Ethereum', 'Litecoin']
tweetsPerDay = 100

for i in range(len(date_list)-1):
    start = date_list[i]
    end = date_list[i+1]
    for coin in coins:
        subprocess.call(['python', 'Exporter.py', \
                         '--since', start, \
                         '--until', end, \
                         '--querysearch', coin, \
                         '--maxtweets', str(tweetsPerDay), \
                         '--toptweets', \
                         '--output', coin+'_'+start+'_'+str(tweetsPerDay)+'.csv'])