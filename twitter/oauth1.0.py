import base64
import json
import random

import twitter
from datetime import datetime
import requests
import time
import random
import tweepy

# from requests_oauthlib import OAuth1Session
# twitter = OAuth1Session(api_info['api_key'],
#                         client_secret=api_info['api_secrete_key'],
#                         resource_owner_key=api_info['access_token'],
#                         resource_owner_secret=api_info['access_token_secrete'])
# url = 'https://api.twitter.com/1.1/statuses/update.json'
# r = twitter.get(url)
# print(r.json())

'''
$ curl --request GET 
  --url 'https://api.twitter.com/1.1/users/search.json?q=soccer' 
  --header 'authorization: OAuth oauth_consumer_key="consumer-key-for-app", 
  oauth_nonce="generated-nonce", oauth_signature="generated-signature", 
  oauth_signature_method="HMAC-SHA1", oauth_timestamp="generated-timestamp", 

'''
URL = 'https://api.twitter.com/1.1/statuses/update.json'

#
# # location given here
# location = "delhi technological university"
#
# # defining a params dict for the parameters to be sent to the API
'''
API key and secret: oauth_consumer_key & oauth_consumer_secret
Access token and secret: oauth_token & oauth_token_secret
'''
def get_nonce():
    """Unique token generated for each request"""
    n = base64.b64encode(
        ''.join([str(random.randint(0, 9)) for i in range(24)]))
    return n

print(str(int(round(time.time()))))
PARAMS = {"include_entities" :"true" ,"oauth_consumer_key" :'' ,"oauth_nonce" :get_nonce()
          ,"oauth_signature_method" :"HMAC-SHA1" ,"oauth_timestamp" :str(int(round(time.time())))
          ,"oauth_token" :'' ,"oauth_version" :"1.0"}
print(PARAMS)


# headers = {
#            "Connection": "close",
#             "User-Agent": "OAuth gem v0.4.4",
#            "Content-Type": "application/x-www-form-urlencoded",
#            }
# headers = {"Accept": "*/*",
#            "Connection": "close",
#             "User-Agent": "OAuth gem v0.4.4",
#            "Content-Type": "application/x-www-form-urlencoded",
#            "Content-Length":"76",
#            "Host": "api.twitter.com"
#            }
#
# # sending get request and saving the response as response object
r = requests.post(url=URL, params=PARAMS ,headers=headers)
#
# # extracting data in json format
data = r.json()
print(data)
#
# r = requests.get('https://api.twitter.com/1.1/users/lookup.json')
# get_tweet('LFC',alznn_api)
