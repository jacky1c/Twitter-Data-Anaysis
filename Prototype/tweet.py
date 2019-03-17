#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 12:09:09 2019
@author: jacky
"""                         
                             
import pandas as pd  
import numpy as np    
import matplotlib.pyplot as plt        
from credentials import *
import tweepy
from tweepy.streaming import StreamListener
from slistener import SListener
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import datetime
import json
from pprint import pprint
from functions import * # self defined functions





# File to save Twitter data
currentDT = datetime.now()
timeStr = currentDT.strftime("%Y-%m-%d_%H:%M:%S")
outfilename = 'SOTU_'+timeStr+'.json'

# Collect data from Twitter API and export to json file
keywords_to_track = ('State of the Union', 'sotu')
#collect_twitter_data(keywords_to_track, 1000, outfilename)    
        
# Load json data from file to python dictionary
with open('SOTU_2019-03-17_14:43:49.json') as infile:
    data = json.load(infile)

# Flatten twitter data
visited_tweet_id_set = set()
tweets_list = flatten_tweets(data, visited_tweet_id_set)

# Create a DataFrame from `twitter data
tweets = pd.DataFrame(tweets_list)
















#
## Print out the first 5 tweets from this dataset
##print(tweets['text'].values[0:5])
#
## Get a Series of tweets that contain a keyword in tweet, quoted tweet, or retweet
#check_word = check_word_in_tweet('immigration', tweets)
#
#
#
#print(np.sum(check_word)/tweets.shape[0])
#
#
#
#
#
#
##sentiment_ram = sentiment[check_word_in_tweet('immigration', tweets)].mean()
##print(sentiment_patriots)
##print(sentiment_ram)
#
#sentiment = analyzeSentiment(tweets, 'Trump')
#
#print(sentiment)
#
##meanTrunp = tweets[check_word_in_tweet('Trump', tweets)].resample('1 h').mean()
#
plotMapTime(tweets, 'Trump', 'Pelosi')
#
#
#
#
plotSentiment(tweets, 'Trump', 'Pelosi')
#
##print(tweets['user-location'].value_counts())
#
#


#
##for t in tweets:
##    if t['user-location'] is 'United States':
##        print(t['text'])
#
#
#



out = open("StatesOut.txt", "+w")


f = open("States.txt", "r")
out.write("{")
#f1 = f.readlines()
while True:
    line1 = f.readline()
    line1len = len(line1)
    line1Cut = line1[0:(line1len-1)]
    
    line2 = f.readline()
    line2len = len(line2)
    line2Cut = line2[0:(line2len-1)]
    
    
    if not line2: break
    print(line1Cut,line2Cut)
    avg= SortByState(tweets, 'Trump', line1Cut, line2Cut, out)
    print("-------")

out.write("}")

    








#














