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

    

# Read tweets about Trump and export time series sentiment score
visited_tweet_id_set = set()
all_Trump_tweets_list = []

with open("TrumpTimeSeries.js", "+w") as outfile:
    outfile.write("var Trump_ScoreByTime = {\n")
    ctr = 0
    print("Trump sentiment score by time:")
    for inFileName in glob.glob('twitter_data/Trump_*', recursive=True):
        with open(inFileName, 'r') as infile:
            # the first key-value pair doesn't have prefix comma
            ctr = ctr + 1
            if ctr != 1:
                outfile.write(",\n")
            # get datetime from file name
            dateTime = inFileName[-24:-5]
            dateTime = FormatDatetime(dateTime)
            data = json.load(infile)
            # Flatten twitter data
            tweets_list = flatten_tweets(data, visited_tweet_id_set)
            all_Trump_tweets_list = all_Trump_tweets_list + tweets_list
            # Create a DataFrame from twitter data
            tweets = pd.DataFrame(tweets_list)
            tweets = tweets.sort_values(by=['created_at'])
            # calculate average sentiment score for this file
            sentimentScore = analyzeSentiment(tweets, 'Trump')
            # write time and sentiment score as key-value pair to output file
            outfile.write("'%s': %f" % (dateTime, sentimentScore))
            print("'%s': %f" % (dateTime, sentimentScore))
        infile.close()
    outfile.write("\n}")
    outfile.close()

# Export sentiment score by state
all_Trump_tweets = pd.DataFrame(all_Trump_tweets_list)

inFile = open("States.txt", "r") 
outFile = open("TrumpStates.js", "+w")
outFile.write("var Trump_ScoreByState = {\n")

print("Trump sentiment score by state:")
# read lines from input file
while True:
    # line1 is state fullname
    line1 = inFile.readline()
    if not line1:  # reach EOF
        break
    # remove break line character at the end
    line1len = len(line1)
    line1Cut = line1[0:(line1len-1)]
    
    # line2 is state abbreviation
    line2 = inFile.readline()
    line2len = len(line2)
    # remove break line character at the end
    if line2[line2len-1] is "\n":
        line2Cut = line2[0:(line2len-1)]
    else:
        line2Cut = line2
    # calculate average sentiment score of that state
    SortByState(all_Trump_tweets, 'Trump', line1Cut, line2Cut, outFile)

outFile.write("\n}")
inFile.close()
outFile.close()


