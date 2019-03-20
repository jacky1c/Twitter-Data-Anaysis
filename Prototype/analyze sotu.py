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


# analyze sotu data
visited_tweet_id_set = set()
with open("SotuTimeSeries.js", "+w") as outfile:
    outfile.write("var TrumpMention_ByTime = {\n")
    ctr = 0
    print("SOTU:")
    for inFileName in glob.glob('SOTU_*', recursive=True):
        with open(inFileName, 'r') as infile:
            ctr = ctr + 1
            dateTime = inFileName[5:-5]
            dateTime = FormatDatetime(dateTime)
            data = json.load(infile)
            tweets_list = flatten_tweets(data, set())
            ds_tweets = pd.DataFrame(tweets_list)
            # calculate average sentiment score for this file
            trump_mention = check_word_in_tweet('Trump', ds_tweets).mean()
            trump_sentiment_score = analyzeSentiment(ds_tweets, 'Trump')
            pelosi_mention = check_word_in_tweet('Pelosi', ds_tweets).mean()
            pelosi_sentiment_score = analyzeSentiment(ds_tweets, 'Pelosi')
            # write to file
            if ctr != 1:
                outfile.write(",\n")
            outfile.write("'%s': %f" % (dateTime, trump_mention))
    outfile.write("\n}")    
