import os
import math
import time
import json
import twint
import requests
import datetime as dt
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None

import twint

# Configure
# c = twint.Config()
# c.Get_replies = "1234082051554529281"
# Configure
c = twint.Config()
c.Resume = "1234082051554529281"
# c.user = "BorisJohnson"
c.Replies = True
c.Lang = 'en'
c.Search = "coronavirus"
# begindate='2020-03-01'
# enddate='2020-06-01 00:00:00'
c.Since = '2020-03-01 00:00:00'
# c.Until = '2020-06-01 00:00:00'
# Run
# twint.run.Profile(c)

# Run
twint.run.Search(c)
reply_tweets = twint.storage.panda.Tweets_df
# reply_tweets = twint.storage.panda.Tweets_df
print(len(reply_tweets.tweet.to_list()))
input()
print(reply_tweets.tweet.to_list())