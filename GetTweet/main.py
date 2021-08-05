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
    since="2020-03-01",
    until="2020-06-01",
    limit=0,
    saved_file="coronavirus_{}.csv",
    lang='en',
)

users = [
    'BorisJohnson', #英國首相
    'jeremycorbyn', #北伊斯靈頓的工黨議員
    'theresa_may', #前英國首相 梅伊 保守黨黨員
    'SadiqKhan', #倫敦市市長
    'DavidDavisMP', #Haltemprice和Howden的國會保守黨議員。
    # 'Nigel_Farage', #Leader of @BrexitParty_UK 脫歐黨黨魁
    # 'Jacob_Rees_Mogg' #保守黨黨員，下議院領袖
    'huwbbc', #威爾斯的新聞記者，主持人和新聞播音員。作為英國BBC新聞的主要主持人
    'EmmaWatson', #英國演員
    'Adele', #英國歌手
    # 'idriselba',  # 據說為了讓人重視假裝自己中獎的演員
    # 'SimonBrodkin',  # 英國喜劇演員
    # 'JohnCleese', #英國演員、編劇和電影製作人
    # 'richardbranson', #理查·查爾斯·尼可拉斯·布蘭森爵士是英國維珍集團的董事長。

    'HKane',    #英超球星 英國足球國家隊隊長 熱刺
    'JHenderson',  #英超球星 利物浦隊長
    'DanielSturridge', #英超球員 利物浦
    'J_Gomez97', #英超球員 利物浦
    'trentaa98', #英超球員 利物浦
    'sterling7', #英超球員 曼城
    'MarcusRashford', #英超球員 曼聯
    'BenChilwell', #英超球員 萊斯特城
    'OfficialTM_3', #英超球員 阿斯頓為拉
    'masonmount_10' #英超球員 切爾西
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
def mention_impact(user):
    c = twint.Config()
    c.Filter_retweets = True
    c.Hide_output = True
    c.Pandas = True
    start_date = datetime.strptime(args.since, '%Y-%m-%d').date()
    end_date = datetime.strptime(args.until, '%Y-%m-%d').date()
    for begindate, enddate in daterange(start_date, end_date):
        print(begindate.strftime("%Y-%m-%d"), enddate.strftime("%Y-%m-%d"))
        start = time.time()
        c.Search = args.keyword.format(user)
        c.Since = begindate.strftime("%Y-%m-%d")
        c.Until = enddate.strftime("%Y-%m-%d")
        twint.run.Search(c)
        pd_tweets = twint.storage.panda.Tweets_df
        print(f'{time.time() - start} s')
        if len(pd_tweets) != 0:
            unique_user = pd_tweets.groupby(
                pd_tweets.user_id.tolist(), as_index=False).size()
            tweet_count = len(pd_tweets)
            unique_user_count = len(unique_user)
            influence_score = ((0.9 ** (unique_user - 1)).sum() /
                               (unique_user_count)) * math.log10(tweet_count)
        else:
            tweet_count = 0
            unique_user_count = 0
            influence_score = 0
        data = {
            'date': [begindate.strftime("%Y/%#m/%#d")],
            'tweet_count': [tweet_count],
            'unique_user_count': [unique_user_count],
            'influence_score': [influence_score],
        }
        print('----------------------------------------------')
        print(user)
        append_data = pd.DataFrame.from_dict(data)
        print(append_data)
        append_data.to_csv(
            args.saved_file.format(user), mode='a',
            header=not os.path.exists(args.saved_file.format(user)),
            index=False
        )
if __name__ == '__main__':
    for user in users:
        mention_impact(user)