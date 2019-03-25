#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 12:09:09 2019
@author: 
    Alexander Biezenski, SID: 200315435
    Shengye Chen, SID: 200354388
    Elizabeth Rayner, SID:200365470
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
trump_mention_dict = {}
trump_sentiment_score_dict = {}
pelosi_mention_dict = {}
pelosi_sentiment_score_dict = {}


# open all SOTU files
for inFileName in glob.glob('twitter_data/SOTU_*', recursive=True):
    with open(inFileName, 'r') as infile:
        dateTime = inFileName[-24:-5]
        dateTime = FormatDatetime(dateTime)
        data = json.load(infile)
        tweets_list = flatten_tweets(data, set())
        ds_tweets = pd.DataFrame(tweets_list)
        # calculate percentage of mentions and average sentiment score
        trump_mention = check_word_in_tweet('Trump', ds_tweets).mean()
        trump_mention_dict[dateTime] = trump_mention
        
        trump_sentiment_score = analyzeSentiment(ds_tweets, 'Trump')
        trump_sentiment_score_dict[dateTime] = trump_sentiment_score
        
        pelosi_mention = check_word_in_tweet('Pelosi', ds_tweets).mean()
        pelosi_mention_dict[dateTime] = pelosi_mention
        
        pelosi_sentiment_score = analyzeSentiment(ds_tweets, 'Pelosi')
        pelosi_sentiment_score_dict[dateTime] = pelosi_sentiment_score
    infile.close()
        
# write result to an output file
with open("SotuTimeSeries.js", "+w") as outfile:
    # Trump mention by time
    print("Trump Mention By Time:")
    outfile.write("var SOTU_TrumpMention_ByTime = {\n")
    ctr = 0
    for dateTime, mention in trump_mention_dict.items():
        ctr = ctr + 1
        # write to file
        if ctr != 1:
            outfile.write(",\n")
        outfile.write("'%s': %f" % (dateTime, mention))
        print("'%s': %f" % (dateTime, mention))
    outfile.write("\n}; \n\n")  
        
    # Pelosi mention by time
    print("Pelosi Mention By Time:")
    outfile.write("var SOTU_PelosiMention_ByTime = {\n")
    ctr = 0
    for dateTime, mention in pelosi_mention_dict.items():
        ctr = ctr + 1
        if ctr != 1:
            outfile.write(",\n")
        outfile.write("'%s': %f" % (dateTime, mention))
        print("'%s': %f" % (dateTime, mention))
    outfile.write("\n}; \n\n") 
        
    # Trump score by time
    print("Trump Score By Time:")
    outfile.write("var SOTU_TrumpScore_ByTime = {\n")
    ctr = 0
    for dateTime, score in trump_sentiment_score_dict.items():
        ctr = ctr + 1
        if ctr != 1:
            outfile.write(",\n")
        outfile.write("'%s': %f" % (dateTime, score))
        print("'%s': %f" % (dateTime, score))
    outfile.write("\n}; \n\n")
        
    # Pelosi score by time
    print("Pelosi Score By Time:")
    outfile.write("var SOTU_PelosiScore_ByTime = {\n")
    ctr = 0
    for dateTime, score in pelosi_sentiment_score_dict.items():
        ctr = ctr + 1
        if ctr != 1:
            outfile.write(",\n")
        outfile.write("'%s': %f" % (dateTime, score))
        print("'%s': %f" % (dateTime, score))
    outfile.write("\n}; \n\n")
outfile.close()      