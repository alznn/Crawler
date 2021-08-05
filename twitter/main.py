import base64
import json
import random
import re
import logging
import sys

import twitter
import pandas as pd
from datetime import datetime
import requests
import time
import random
import urllib.parse
import tweepy
from influxdb import InfluxDBClient

file = open('info.json','r',encoding='utf-8')
api_info = json.load(file)
PL_teams =['@Wolves','@BurnleyOfficial','@Everton','@LCFC','@NUFC','@NorwichCityFC','@NorwichCityFC','@SouthamptonFC','@WatfordFC']
#LFC

alznn_api = twitter.Api(consumer_key= api_info['api_key'],
                  consumer_secret=api_info['api_secrete_key'],
                  access_token_key=api_info['access_token'],
                  access_token_secret=api_info['access_token_secrete'],tweet_mode='extended')
#
date = []
favorite_count = []
retweet_count=[]
hashtags = []
id = []
text = []
source = []

client = InfluxDBClient(host='my server', port='My port', database="My database")

account_list = ["Arsenal", "SheffieldUnited", "AVFCOfficial", "afcbournemouth", "OfficialBHAFC",
                    "BurnleyOfficial", "ChelseaFC", "CPFC", "Everton", "LCFC", "LFC", "ManCity", "ManUtd", "NUFC",
                    "NorwichCityFC",
                    "SouthamptonFC", "SpursOfficial", "WatfordFC", "WestHam", "Wolves"]
measurement = "Reply"

def insert_influxdb(measurement, team,replies,count):
    print("get in insert_infuxdb!!!!!!!!!!!!!!!!")
    # print(replies)
    #  header = ['timestamp', 'reply_id', 'reply_screen_name', 'full_text', 'in_reply_to_status_id','in_reply_to_screen_name', 'replay_location']
    ans = []
    for index in range(len(replies['reply_id'])):
        data = {}
        data['measurement'] = measurement
        data['time'] = str(replies['timestamp'][index])
        tags = {}
        tags['team'] = team
        tags['in_reply_to_status_id'] = str(replies['in_reply_to_status_id'][index])
        fields = {}
        fields['counter'] = str(replies['counter'][index])
        fields['reply_id'] = str(replies['reply_id'][index])
        fields['reply_screen_name'] = replies['reply_screen_name'][index]
        fields['full_text'] = replies['full_text'][index]
        # fields['in_reply_to_status_id'] = data['in_reply_to_status_id'][index]
        fields['in_reply_to_screen_name'] = replies['in_reply_to_screen_name'][index]
        fields['replay_location'] = replies['replay_location'][index]
        data['tags'] = tags
        data['fields'] = fields

        # print(data)
        json_data = json.dumps(data)
        ans.append(data)
    with open(str(team)+'_data_check'+str(count)+'.json','w',encoding='utf-8') as f:
        json.dump(ans,f,indent=2)
    print("file write down!!!!!!!!!!!!")
    client.write_points(ans)
    print("check influx Database !!!!!!!!!!!")
    return

def get_reply_usr(user_name='BBCNews',api=alznn_api):
    tweet_id = '1241072514937188352'
    auth = tweepy.OAuthHandler(consumer_key=api_info['api_key'], consumer_secret=api_info['api_secrete_key'])
    auth.set_access_token(api_info['access_token'], api_info['access_token_secrete'])
    api = tweepy.API(auth)
    user = api.get_user(screen_name=user_name,per_page=1,page='1247600027700203521' )
    # print(user)

        # user.id

def get_reply(user_name='BBCNews',api=alznn_api):
    total_reply_df = []
    reply_screen_name = []
    reply_id = []
    full_text = []
    in_reply_to_status_id = []
    in_reply_to_screen_name = []
    replay_location = []
    timestamp = []
    counter = []

    print("get in")
    #Nov 30 22:00:00 +0000 2019	1200897292036976640
    tweet_id = ''

    #alznn_api = twitter.Api(consumer_key= api_info['api_key'],
                  # consumer_secret=api_info['api_secrete_key'],
                  # access_token_key=api_info['access_token'],
                  # access_token_secret=api_info['access_token_secrete'],tweet_mode='extended')
    auth = tweepy.OAuthHandler(consumer_key=api_info['api_key'], consumer_secret=api_info['api_secrete_key'])
    auth.set_access_token(api_info['access_token'], api_info['access_token_secrete'])
    # api = tweepy.API(auth,wait_on_rate_limit=True )
    api = tweepy.API(auth)


    replies = tweepy.Cursor(api.search, q='to:{}'.format(user_name),
                            since_id=tweet_id, tweet_mode='extended').items()
    # print(len(replies))
    count =1
    while True:
        '''
        reply = replies.next()
        if not hasattr(reply, 'in_reply_to_status_id_str'):
            continue
        if reply.in_reply_to_status_id == tweet_id:
            print("=======================")
            logging.info("reply of tweet:{}".format(reply.full_text))
            reply_id.append(str(reply.id))
            reply_screen_name.append(reply.author.screen_name)
            replay_location.append(reply.author.location)
            full_text.append(str(reply.full_text).replace('\n', '。'))
            in_reply_to_status_id.append(str(reply.in_reply_to_status_id))
            in_reply_to_screen_name.append(reply.in_reply_to_screen_name)
            timestamp.append(str(reply.created_at.strftime("%m-%d-%Y, %H:%M:%S")))
        else:
            print("********************************************")
            # print(reply.id)
            # print(reply.author.screen_name)
            # print(reply.full_text)
            reply_id.append(reply.id)
            reply_screen_name.append(reply.author.screen_name)
            replay_location.append(reply.author.location)
            full_text.append(str(reply.full_text).replace('\n', '。'))
            in_reply_to_status_id.append(str(reply.in_reply_to_status_id))
            in_reply_to_screen_name.append(str(reply.in_reply_to_screen_name))
            timestamp.append(reply.created_at.strftime("%m-%d-%Y, %H:%M:%S"))
        print(count)
        count += 1
        counter.append(count)
        header = ['counter', 'timestamp', 'reply_id', 'reply_screen_name', 'full_text', 'in_reply_to_status_id',
                  'in_reply_to_screen_name', 'replay_location']
        current_df = pd.DataFrame(list(
            zip(counter, timestamp, reply_id, reply_screen_name, full_text, in_reply_to_status_id,
                in_reply_to_screen_name,
                replay_location)), columns=header)
        current_df = current_df.sort_values(by=['reply_id'])

        print(current_df.size)

        current_df.to_csv(str(user_name) + '_reply' + str(count) + '.csv', sep='\t', encoding='utf-8',
                          index=False)
        total_reply_df.append(current_df)

        insert_influxdb(measurement='Replies', team=user_name, replies=current_df,count=count)
        input()
        '''
        try:
            reply = replies.next()
            print(reply)
            input()
            if not hasattr(reply, 'in_reply_to_status_id_str'):
                continue
            if reply.in_reply_to_status_id == tweet_id:
                print("=======================")
                logging.info("reply of tweet:{}".format(reply.full_text))
                reply_id.append(reply.id)
                reply_screen_name.append(reply.author.screen_name)
                replay_location.append(reply.author.location)
                full_text.append(str(reply.full_text).replace('\n', '。'))
                in_reply_to_status_id.append(reply.in_reply_to_status_id)
                in_reply_to_screen_name.append(reply.in_reply_to_screen_name)
                timestamp.append(reply.created_at.strftime("%m-%d-%Y, %H:%M:%S"))
            else:
                # print("********************************************")
                print(reply.id)
                print(reply.author.screen_name)
                print(reply.full_text)
                reply_id.append(reply.id)
                reply_screen_name.append(reply.author.screen_name)
                replay_location.append(reply.author.location)
                full_text.append(str(reply.full_text).replace('\n', '。'))
                in_reply_to_status_id.append(str(reply.in_reply_to_status_id))
                in_reply_to_screen_name.append(reply.in_reply_to_screen_name)
                timestamp.append(reply.created_at.strftime("%m-%d-%Y, %H:%M:%S"))
            print(count)
            count+=1
            counter.append(count)
            header = ['counter','timestamp', 'reply_id', 'reply_screen_name', 'full_text', 'in_reply_to_status_id',
                      'in_reply_to_screen_name', 'replay_location']
            current_df = pd.DataFrame(list(
                zip(counter,timestamp, reply_id, reply_screen_name, full_text, in_reply_to_status_id,
                    in_reply_to_screen_name,
                    replay_location)), columns=header)
            current_df = current_df.sort_values(by=['reply_id'])
            #
            print(current_df.size)
            #
            current_df.to_csv(str(user_name) + '_reply' + str(count) + '.csv', sep='\t', encoding='utf-8',
                              index=False)
            # total_reply_df.append(current_df)
            #
            insert_influxdb(measurement='Replies', team=user_name, replies=current_df,count = count)
            input()
            # if count*1500 == 0:
            #     print(len(timestamp))
            #     print(len(reply_screen_name))
            #     print(len(full_text))
            #
            #     header = ['timestamp', 'reply_id', 'reply_screen_name', 'full_text', 'in_reply_to_status_id',
            #               'in_reply_to_screen_name', 'replay_location']
            #     current_df = pd.DataFrame(list(
            #         zip(timestamp, reply_id, reply_screen_name, full_text, in_reply_to_status_id,
            #             in_reply_to_screen_name,
            #             replay_location)), columns=header)
            #     current_df = current_df.sort_values(by=['timestamp'])
            #
            #     print(current_df.size)
            #
            #     current_df.to_csv(str(user_name) + '_reply' + str(count) + '.csv', sep='\t', encoding='utf-8',
            #                       index=False)
            #     total_reply_df.append(current_df)
            #     timestamp.clear()
            #     reply_id.clear()
            #     reply_screen_name.clear()
            #     full_text.clear()
            #     in_reply_to_status_id.clear()
            #     in_reply_to_screen_name.clear()
            #     replay_location.clear()
        except tweepy.RateLimitError as e:
            logging.error("Twitter api rate limit reached".format(e))
            # print(len(timestamp))
            # print(len(reply_screen_name))
            # print(len(full_text))
            #
            # header = ['counter','timestamp', 'reply_id', 'reply_screen_name', 'full_text', 'in_reply_to_status_id',
            #           'in_reply_to_screen_name', 'replay_location']
            # current_df = pd.DataFrame(list(
            #     zip(counter,timestamp, reply_id, reply_screen_name, full_text, in_reply_to_status_id,
            #         in_reply_to_screen_name,
            #         replay_location)), columns=header)
            # current_df = current_df.sort_values(by=['timestamp'])
            #
            # print(current_df.size)
            #
            # current_df.to_csv(user_name + '_reply' + count + '.csv', sep='\t', encoding='utf-8',
            #                   index=False)
            # #(measurement, team,data,)
            # insert_influxdb(measurement = 'Replies',team = user_name,replies = current_df)
            # total_reply_df.append(current_df)
            time.sleep(900)
            # sys.stdout.flush()
            continue

        except tweepy.TweepError as e:
            logging.error("Tweepy error occured:{}".format(e))
            print(len(timestamp))
            print(len(reply_screen_name))
            print(len(full_text))

            header = ['counter','timestamp', 'reply_id', 'reply_screen_name', 'full_text', 'in_reply_to_status_id',
                      'in_reply_to_screen_name', 'replay_location']
            current_df = pd.DataFrame(list(
                zip(counter,timestamp, reply_id, reply_screen_name, full_text, in_reply_to_status_id,
                    in_reply_to_screen_name,
                    replay_location)), columns=header)
            current_df = current_df.sort_values(by=['counter'])

            print("df size:",current_df.size)

            current_df.to_csv(str(user_name) + '_reply' + str(count) + '.csv', sep='\t', encoding='utf-8',
                              index=False)
            total_reply_df.append(current_df)

            insert_influxdb(measurement='Reply', team=user_name, replies=current_df,count=count)

            counter.clear()
            timestamp.clear()
            reply_id.clear()
            reply_screen_name.clear()
            full_text.clear()
            in_reply_to_status_id.clear()
            in_reply_to_screen_name.clear()
            replay_location.clear()
            print("time to sleep")
            time.sleep(900)
            # sys.stdout.flush()
            continue
            # break

        except StopIteration:
            break

        except Exception as e:
            logging.error("Failed while fetching replies {}".format(e))
            break

    # result = pd.concat(total_reply_df)
    # result = result.sort_values(by=['timestamp'])
    # result = result.drop_duplicates(subset='id')
    # result.to_csv(user_name + '_reply.csv', sep='\t', encoding='utf-8', index=False)

    return total_reply_df


def decode(tweets):
    '''
    :param tweets:
        source  -=[link]
        lang = en
        id_str = string id
    :return: pandas dataframe
    '''
    for tweet in tweets:
        # print(tweet)
        # input()
        date.append(tweet.created_at)
        id.append(tweet.id)
        text.append(str(tweet.full_text).replace('\n','。'))
        favorite_count.append(tweet.favorite_count)
        retweet_count.append(tweet.retweet_count)
        # print(tweet.hashtags)
        tmp = []
        if tweet.hashtags:
            for ht in tweet.hashtags:
                tmp.append(ht.text)
        else:
            tmp.append("#NaN")
        hashtags.append(tmp)
    # print(date[0])
    # print(id[0])
    # print(text[0])
    # print(hashtags[0])
    # print(favorite_count)
    # print(retweet_count)
    # todf = {'date': date,'id': id,'date': date,'date': date,'date': date,'date': date}
    header = ['date','id','text','hashtags','favorite_count','retweet_count']
    df = pd.DataFrame(list(zip(date, id,text,hashtags,favorite_count,retweet_count)), columns=header)
    # df = pd.DataFrame(data = todf)
    print("done")
    return df
    # pass
def get_tweet(user_name='BBCNews',api=alznn_api):
    tweet_df =[]
    #BBCUK -> BBCNews
    timeline = api.GetUserTimeline(screen_name=user_name, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    count = 0
    while True:
        tweets = api.GetUserTimeline(
            screen_name=user_name, max_id=earliest_tweet, count=200,include_rts =True
        )
        new_earliest = min(tweets, key=lambda x: x.id).id
        count+=1
        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
                                 # datetime.fromtimestamp(1172969203.1)
            timestamp = round(float(earliest_tweet) / 1000, 3)
            # print("getting tweets before [in while]:", earliest_tweet)
            # print(type(tweets))
            current_tweet = decode(tweets)
            current_tweet=current_tweet.sort_values(by=['id'])
            current_tweet.to_csv(user_name +str(count)+ '.csv', sep='\t', encoding='utf-8', index=False)
            tweet_df.append(current_tweet)
            timeline += tweets
    result = pd.concat(tweet_df)
    result = result.sort_values(by=['id'])
    result = result.drop_duplicates(subset='id')
    result.to_csv(user_name+'.csv',sep = '\t',encoding = 'utf-8', index=False)
    print(len(timeline))

    return timeline
    # print(timeline)
if __name__ == '__main__':
    for team in PL_teams:
        data = get_reply(user_name='@LFC',api=alznn_api)
        # result = pd.concat(data)
        # data = get_reply(user_name=team,api=alznn_api)
        # result = data.sort_values(by=['timestamp'])
        # result = result.drop_duplicates(subset='timestamp')
        # result.to_csv(team + '_reply.csv', sep='\t', encoding='utf-8', index=False)
        # input()