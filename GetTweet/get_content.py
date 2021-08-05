import os
import math
import time
import json
import codecs
import requests
import collections
import datetime as dt
import pandas as pd
import twint
pd.options.mode.chained_assignment = None
# this enables us for rewriting dataframe to previous variable
#  from twitterscraper import query_tweets
from datetime import datetime
from argparse import Namespace

name = ""
args = Namespace(
    keyword="coronavirus (@{})",
    since="2020-05-25",
    until="2020-06-01",
    limit=0,
    saved_file="coronavirus_content_{}.csv",
    lang='en',
)

users = [
    'BorisJohnson', #英國首相
    '10DowningStreet',  # 英國首相官方帳號
    'Conservatives',  # 保守黨官方帳號
    'theresa_may', #前英國首相 梅伊 保守黨黨員
    'DavidDavisMP', #Haltemprice和Howden的國會保守黨議員。
    'Jacob_Rees_Mogg' #保守黨黨員，下議院領袖
    
    'SadiqKhan', #倫敦市市長
    'MayorofLondon',  # 倫敦市長官方帳號

    'UKLabour',  # 工黨官方帳號
    'jeremycorbyn', #北伊斯靈頓的工黨議員
    'HarrietHarman' #前工黨黨魁
    'Keir_Starmer' #工黨
    'JackDromeyMP' #工黨
    'VirendraSharma' #工黨

    'Nigel_Farage', # 脫歐黨黨魁官方帳號
    'Nigel_Farage', #Leader of @BrexitParty_UK 脫歐黨黨魁
]

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__json__'):
            return obj.__json__()
        elif isinstance(obj, collections.abc.Iterable):
            return list(obj)
        elif isinstance(obj, dt.datetime):
            return obj.isoformat()
        elif hasattr(obj, '__getitem__') and hasattr(obj, 'keys'):
            return dict(obj)
        elif hasattr(obj, '__dict__'):
            # save all key value pairs
            # return {member: getattr(obj, member)
            #         for member in dir(obj)
            #         if not member.startswith('_') and
            #         not hasattr(getattr(obj, member), '__call__')}
            return {
                member: getattr(obj, member) for member in [
                    'username', 'user_id', 'timestamp', 'text'
                ]
            }
        return json.JSONEncoder.default(self, obj)
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield (start_date + dt.timedelta(n), start_date + dt.timedelta(n + 1))
def get_content(user):

    start_date = datetime.strptime(args.since, '%Y-%m-%d').date()
    end_date = datetime.strptime(args.until, '%Y-%m-%d').date()

    for begindate, enddate in daterange(start_date, end_date):
        id_list = []
        created_at = []
        date = []
        content = []
        reply_count = 0  # initial count
        print(begindate.strftime("%Y-%m-%d"), enddate.strftime("%Y-%m-%d"))

        start = time.time()
        print('----------------------------------------------')
        print('Start searching user post')
        c = twint.Config()
        c.Lang = 'en'
        c.Search = "coronavirus"
        c.Username = user
        c.Since = begindate.strftime("%Y-%m-%d")
        c.Until = enddate.strftime("%Y-%m-%d")
        c.Pandas = True
        twint.run.Search(c)
        pd_tweets = twint.storage.panda.Tweets_df
        '''
        ['cashtags', 'conversation_id', 'created_at', 'date', 'day', 
        'geo', 'hashtags', 'hour', 'id', 'link', 'name', 'near', 'nlikes', 
        'nreplies', 'nretweets', 'place', 'quote_url', 'reply_to', 'retweet', 
        'retweet_date', 'retweet_id', 'search', 'source', 'timezone', 'trans_dest', 
        'trans_src', 'translate', 'tweet', 'user_id', 'user_id_str', 'user_rt', 'user_rt_id', 'username']
        '''
        # input()
        print('Done search')
        print('----------------------------------------------')
        if len(pd_tweets) != 0:
            id_list.extend(pd_tweets.conversation_id.tolist())
            created_at.extend(pd_tweets.created_at.tolist())
            date.extend(pd_tweets.date.tolist())
            content.extend(pd_tweets.tweet.tolist())
            content = [c.replace('\n','') for c in content]
        # else:
        #     tweet_count = 0
        #     unique_user_count = 0
        #     influence_score = 0
            data = {
                'id': id_list,
                'created_at': created_at,
                'date': date,
                'content':content,
                # 'influence_score': [influence_score],
            }
            print('----------------------------------------------')
            print(user)
            append_data = pd.DataFrame.from_dict(data)
            print(append_data)
            # input()
            append_data.to_csv(
                args.saved_file.format(user), mode='a',
                header=not os.path.exists(args.saved_file.format(user)),
                index=False
            )
        time.sleep(time.time() - start)

if __name__ == '__main__':
    for user in users:
        get_content(user)