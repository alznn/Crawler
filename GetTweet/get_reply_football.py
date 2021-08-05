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

# from twitterscraper import query_tweets
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


def reply_influence(user):
    id_list = []

    start_date = datetime.strptime(args.since, '%Y-%m-%d').date()
    end_date = datetime.strptime(args.until, '%Y-%m-%d').date()
    for begindate, enddate in daterange(start_date, end_date):
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
        print('Done search')
        print('----------------------------------------------')
        time.sleep(time.time() - start)

        # Store post id in id_list[]
        for i in range(len(pd_tweets)):
            id_list.append(pd_tweets['id'][i])
        print('id stored')
        print('id_list: ', len(id_list))

        if len(id_list) != 0:
            start = time.time()
            print('----------------------------------------------')
            print('Start searching reply post to user')
            reply = twint.Config()
            reply.Lang = 'en'
            reply.Filter_retweets = True
            reply.Hide_output = True
            reply.Pandas = True
            reply.To = user
            reply.Since = begindate.strftime("%Y-%m-%d")
            reply.Until = enddate.strftime("%Y-%m-%d")
            twint.run.Search(reply)
            reply_tweets = twint.storage.panda.Tweets_df
            print('Done search reply')
            print('----------------------------------------------')

            # id: current post id
            # conversation_id: original post id, i.e. the post id that is replied
            for r in range(len(reply_tweets)):
                for i in range(len(id_list)):
                    if reply_tweets['conversation_id'][r] == id_list[i]:
                        reply_count = reply_count + 1

            print('reply count: ', reply_count)

        else:
            reply_count = 0

        print(f'{time.time() - start} s')

        # if len(pd_tweets) != 0:
        #     unique_user = pd_tweets.groupby(
        #         pd_tweets.user_id.tolist(), as_index=False).size()

        #     tweet_count = len(pd_tweets)
        #     unique_user_count = len(unique_user)
        #     influence_score = ((0.9 ** (unique_user - 1)).sum() /
        #                        (unique_user_count)) * math.log10(tweet_count)
        # else:
        #     tweet_count = 0
        #     unique_user_count = 0
        #     influence_score = 0

        data = {
            'user': [user],
            'date': [begindate.strftime("%Y/%#m/%#d")],
            'tweet_count': [len(pd_tweets)],
            'influence_score': [reply_count],
            'total post': [len(id_list)]
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

        time.sleep(time.time() - start)

    id_list.clear()

if __name__ == '__main__':
    for user in users:
        reply_influence(user)
    # get_reply_date('1234082051554529281','2020-03-01','2020-06-01')