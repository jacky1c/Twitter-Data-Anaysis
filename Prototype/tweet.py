#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 12:09:09 2019

@author: jacky

from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
from slistener import SListener

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# Consumer key authentication
auth = OAuthHandler(consumer_key, consumer_secret)

# Access key authentication
auth.set_access_token(access_token, access_token_secret)

# Set up the API with the authentication handler
api = API(auth)



# Set up words to track
keywords_to_track = ('#rstats', '#python')

# Instantiate the SListener object 
listen = SListener(api)

# Instantiate the Stream object
stream = Stream(auth, listen)

# Begin collecting data
stream.filter(track = keywords_to_track)

print(stream.sample())
"""
"""
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import json



auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)



def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status


tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse


class MyListener(tweepy.StreamListener):
    def on_data(self, data):
        try:
            with open('FILENAME.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#HASHTAG_TO_SEARCH'])
"""                            

                             
                             
from credentials import *
import tweepy
from slistener import SListener
import json
from tweepy.streaming import StreamListener




# Consumer key authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

# Access key authentication
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Set up the API with the authentication handler
api = tweepy.API(auth)

# Set up words to track
keywords_to_track = ('red')

# Instantiate the SListener object
#listen = SListener()
listen = SListener(api)

# Instantiate the Stream object
stream = tweepy.Stream(auth, listen)

print("Before")

# Begin collecting data
#stream.filter(track = '#Trump', languages=["en"])
print("after")

api1 = tweepy.API(auth)
api2 = tweepy.API(auth)
api3 = tweepy.API(auth)
api4 = tweepy.API(auth)
#for tweet in tweepy.Cursor(api.search, q='#Trump',rpp=100).items(10):
#    print (tweet.created_at, tweet.text)
#This line is whats actually being used
test = tweepy.Cursor(api1.search, q=keywords_to_track, languages=["en"]).items(10)

num = 0

for twit in test:
    num = num + 1
    print(num, ".")
    print(twit.user.screen_name)
    print(twit.text)

    #print(twit.retweeted_status)
    print()
    #tweet = json.loads(twit)

tweet_json = tweepy.Cursor(api1.search, q=keywords_to_track, languages=["en"]).items(1)

#tweet = json.loads(tweet_json)
#print(tweet_json.id)

# We create a tweet list as follows:
tweets = api2.user_timeline(screen_name="realDonaldTrump", count=200)
print("Number of tweets extracted: {}.\n".format(len(tweets)))

# We print the most recent 5 tweets:
#print("5 recent tweets:\n")
for tweet in tweets[:5]:
    print(tweet.text)
    print("RETWEETS")
    rt = api3.retweets(tweet.id)
    for tt in rt[:5]:
        print(tt.user.screen_name)
    qt = api4.quotes(tweet.id)
    print()
