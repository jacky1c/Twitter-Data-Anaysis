#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 12:09:09 2019

@author: jacky
"""                         
                             
import pandas as pd  
import numpy as np              
from credentials import *
import tweepy
from tweepy.streaming import StreamListener
from slistener import SListener
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import datetime
import json
import glob
from pprint import pprint
from functions import * # self defined functions


## File to save Twitter data
#currentDT = datetime.datetime.now()
#timeStr = currentDT.strftime("%Y-%m-%d_%H:%M:%S")
#outfilename = 'superbowl_'+timeStr+'.json'
#
## Collect data from Twitter API and export to json file
#collect_twitter_data(outfilename)    
        
# Load json data from file to python dictionary
tweets_list = []
for filename in glob.glob('superbowl_2019-02-03*', recursive=True):
    with open(filename, 'r') as infile:
        data = json.load(infile)
        # Flatten twitter data
        tweets_list = tweets_list + flatten_tweets(data)

# Create a DataFrame from `twitter data
tweets = pd.DataFrame(tweets_list)
tweets = tweets.sort_values(by=['created_at'])

# Print out the first 5 tweets from this dataset
#print(tweets['text'].values[0:5])

# Get a Series of tweets that contain a keyword in tweet, quoted tweet, or retweet
#check_word = check_word_in_tweet('ram', tweets)
#print(np.sum(check_word)/tweets.shape[0])

# Instantiate sentiment intensity analyzer
sid = SentimentIntensityAnalyzer()

# Generate sentiment scores by applying polarity_scores function to all tweet text
sentiment_scores = tweets['text'].apply(sid.polarity_scores)

# Extract compound from sentiment score. Options are: neg, neu, pos, compound
sentiment = sentiment_scores.apply(lambda x: x['compound'])

# Calculate average compound score for tweets that contain keyword
sentiment_patriots = sentiment[check_word_in_tweet('patriots', tweets)].mean()
sentiment_ram = sentiment[check_word_in_tweet('ram', tweets)].mean()
print("patriots: ", sentiment_patriots)
print("ram: ",sentiment_ram)

plotMapTime(tweets, 'patriots', 'ram')