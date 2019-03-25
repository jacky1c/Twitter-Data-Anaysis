#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 13:14:44 2019
@author: 
    Alexander Biezenski, SID: 200315435
    Shengye Chen, SID: 200354388
    Elizabeth Rayner, SID:200365470
"""
import json
import os
import tweepy
from tweepy.streaming import StreamListener
from slistener import SListener
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt  
import numpy as np   
from datetime import datetime
import glob


def collect_twitter_data(keywords_to_track, n, outfilename):
    """Collect tweets through Twitter API
    
    Arguments:
        keywords_to_track {tuple} -- tuple of keywords
        n {integer} -- number of tweets per harvest
        outfilename {string} -- name of output file
    """

    # =============================================================================
    # CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, and ACCESS_SECRET are assigned by Twitter
    # =============================================================================

    # Consume:
    CONSUMER_KEY    = 'azhIXA4y3kR5xLcceOpHyLxtU'
    CONSUMER_SECRET = 'YWmMDQaGsck3J9Suboj5Pv6r6UhZ7CJozGV0srcQXk8uW0Mjfr'

    # Access:
    ACCESS_TOKEN  = '1955396544-vbAEUgorMO14epJ808JrthxKfxh3PULVtRv6V84'
    ACCESS_SECRET = 'thT5XIRYYq1Qbt9rnSVUzworHwmsKH0cY0QQta1jkiGKz'

    # Consumer key authentication
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    # Access key authentication
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    
    # Set up the API with the authentication handler
    api = tweepy.API(auth)
    
    api.sleep_on_rate_limit = True
    
    # Instantiate the SListener object
    listen = SListener(api)
    
    # Instantiate the Stream object
    stream = tweepy.Stream(auth, listen)
    
    # Begin collecting data
    tweet_data = tweepy.Cursor(api.search, q=keywords_to_track, languages=["en"]).items(n)
    
    # Export tweets to file
    script_dir = os.path.dirname(__file__)
    rel_path = "twitter_data/" + outfilename
    abs_file_path = os.path.join(script_dir, rel_path)
    ctr = 0
    with open(abs_file_path,'w') as outfile:
        outfile.write('[')
        for tweet in tweet_data:
            ctr = ctr+1
            if ctr != 1:
                outfile.write(',')
            json.dump(tweet._json, outfile)
        outfile.write(']')   
        outfile.close()

def flatten_tweets(tweets_dict_list, visited_tweet_id_set):
    """ Flattens out tweet dictionaries so relevant JSON is in a top-level dictionary.
    Attributes:
        user-screen_name {string}
        created_at {datetime}
        user-location {string}
        user-place-fullname {string}
        user-place-country-code {string}

    Arguments:
        tweets_dict_list {list} -- list of tweets
        visited_tweet_id_set {set} -- set of visited tweet ID
    
    Returns:
        list -- list of flattened tweets
    """
    tweets_list = []
    
    # Iterate through each tweet
    for tweet_obj in tweets_dict_list:
        # Store the user screen name, timestamp, and location
        tweet_obj['user-screen_name'] = tweet_obj['user']['screen_name']
        tweet_obj['created_at'] =  pd.to_datetime(tweet_obj['created_at'])
        tweet_obj['user-location'] = tweet_obj['user']['location']
        if tweet_obj['place'] is not None:
            tweet_obj['user-place-fullname'] = tweet_obj['place']['full_name']
            tweet_obj['user-place-country-code'] = tweet_obj['place']['country_code']        
        # Check if this is a 140+ character tweet
        if 'extended_tweet' in tweet_obj:
            tweet_obj['text'] = tweet_obj['text'] + tweet_obj['extended_tweet']['full_text']
        
        # If tweet hasn't been visited, add to tweets list
        if tweet_obj['id'] not in visited_tweet_id_set:
            tweets_list.append(tweet_obj)
            visited_tweet_id_set.add(tweet_obj['id'])
    
        # Check if this is a retweet
        if 'retweeted_status' in tweet_obj:
            # Treat the retweet and original tweet as two different tweets
            # Store the user screen name, timestamp, and location
            retweet_obj = {}
            retweet_obj['user-screen_name'] = tweet_obj['retweeted_status']['user']['screen_name']
            retweet_obj['created_at'] =  pd.to_datetime(tweet_obj['retweeted_status']['created_at'])
            retweet_obj['user-location'] = tweet_obj['retweeted_status']['user']['location']
            if tweet_obj['retweeted_status']['place'] is not None:
                retweet_obj['user-place-fullname'] = tweet_obj['retweeted_status']['place']['full_name']
                retweet_obj['user-place-country-code'] = tweet_obj['retweeted_status']['place']['country_code']
            retweet_obj['text'] = tweet_obj['retweeted_status']['text']
            if 'extended_tweet' in tweet_obj['retweeted_status']:
                retweet_obj['text'] = retweet_obj['text'] + tweet_obj['retweeted_status']['extended_tweet']['full_text']
            # If retweet hasn't been visited, add retweet to tweet list
            if tweet_obj['retweeted_status']['id'] not in visited_tweet_id_set:
                tweets_list.append(retweet_obj)
                visited_tweet_id_set.add(tweet_obj['retweeted_status']['id'])
            
        # Check if this is a quoted tweet
        if 'quoted_status' in tweet_obj:
            # Treat the quoted tweet and quoting tweet as two different tweets
            # Store the user screen name, timestamp, and location
            quoting_tweet_obj = {}
            quoting_tweet_obj['user-screen_name'] = tweet_obj['quoted_status']['user']['screen_name']
            quoting_tweet_obj['created_at'] =  pd.to_datetime(tweet_obj['quoted_status']['created_at'])
            quoting_tweet_obj['user-location'] = tweet_obj['quoted_status']['user']['location']
            if tweet_obj['quoted_status']['place'] is not None:
                quoting_tweet_obj['user-place-fullname'] = tweet_obj['quoted_status']['place']['full_name']
                quoting_tweet_obj['user-place-country-code'] = tweet_obj['quoted_status']['place']['country_code']
            quoting_tweet_obj['text'] = tweet_obj['quoted_status']['text']
            if 'extended_tweet' in tweet_obj['quoted_status']:
                quoting_tweet_obj['text'] = quoting_tweet_obj['text'] + tweet_obj['quoted_status']['extended_tweet']['full_text']
            # If quoting tweet hasn't been visited, add quoting tweet to tweet list
            if tweet_obj['quoted_status']['id'] not in visited_tweet_id_set:
                tweets_list.append(quoting_tweet_obj)
                visited_tweet_id_set.add(tweet_obj['quoted_status']['id'])
            
    return tweets_list


def check_word_in_tweet(word, data):
    """Checks if a word is in a Twitter dataset's text. 
    Checks text and extended tweet (140+ character tweets) for tweets.
    Returns a logical pandas Series.
    
    
    Arguments:
        word {string} -- keyword to find
        data {dataframe} -- tweets
    
    Returns:
        series -- logical pandas Series
    """

    contains_column = data['text'].str.contains(word, case = False)
    return contains_column


def plotMapTime(ds_tweets, word1, word2):
    """Plot percentage of mentions by time
    
    Arguments:
        ds_tweets {dataframe} -- dataframe of tweets
        word1 {string} -- keyword 1
        word2 {string} -- keyword 2
    """

    ds_tweets['word1'] = check_word_in_tweet(word1, ds_tweets)
    ds_tweets['word2'] = check_word_in_tweet(word2, ds_tweets)

    # Convert index to a time
    ds_tweets['word1'].index = pd.to_datetime(ds_tweets.index, unit='s')
    ds_tweets['word2'].index = pd.to_datetime(ds_tweets.index, unit='s')

    # Resample seconds to minutes and calcualte average
    mean1 = ds_tweets['word1'].resample('1 min').mean()
    mean2 = ds_tweets['word2'].resample('1 min').mean()

    # start to plot on graph
    plt.plot(mean1.index.minute, mean1, color = 'green')
    plt.plot(mean2.index.minute, mean2, color = 'blue')

    plt.xlabel('Minute'); plt.ylabel('Frequency')
    plt.title('Language mentions over time')
    plt.legend((word1, word2))
    plt.show()


def analyzeSentiment(ds_tweets, word):
    """Calculate sentiment score of all tweets that contain a keyword and return average sentiment score
    
    Arguments:
        ds_tweets {dataframe} -- tweets
        word {string} -- keyword to search
    
    Returns:
        float -- average sentiment score
    """

    # Instantiate sentiment intensity analyzer
    sid = SentimentIntensityAnalyzer()

    # Generate sentiment scores by applying polarity_scores function to all tweet text
    sentiment_scores = ds_tweets['text'].apply(sid.polarity_scores)

    # Extract compound from sentiment score. Options are: neg, neu, pos, compound
    sentiment = sentiment_scores.apply(lambda x: x['compound'])

    # Calculate average compound score for tweets that contain keyword
    sentimentAnalysis = sentiment[check_word_in_tweet(word, ds_tweets)].mean()
    
    return sentimentAnalysis


def plotSentiment(ds_tweets, word1, word2):
    """Plot sentiment by time
    
    Arguments:
        ds_tweets {dataframe} -- dataframe of tweets
        word1 {string} -- keyword1
        word2 {string} -- keyword2
    """

    ds_tweets['sentiment1'] = analyzeSentiment(ds_tweets, word1) 
    ds_tweets['sentiment1'].index = pd.to_datetime(ds_tweets.index, unit='s')
    sentiment1 = ds_tweets['sentiment1'].resample('1 min').mean()
    
    
    ds_tweets['sentiment2'] = analyzeSentiment(ds_tweets, word2)
    ds_tweets['sentiment2'].index = pd.to_datetime(ds_tweets.index, unit='s')
    sentiment2 = ds_tweets['sentiment2'].resample('1 min').mean()
    
    plt.plot(sentiment1.index.minute, sentiment1, color = 'green')
    plt.plot(sentiment2.index.minute, sentiment2, color = 'blue')

    plt.xlabel('Minute')
    plt.ylabel('Sentiment')
    plt.title('Sentiment of data science languages')
    plt.legend((word1, word2))
    plt.show()

    
def to_str(var):
    """Convert a value to string

    Reference: #https://stackoverflow.com/questions/24914735/convert-numpy-list-or-float-to-string-in-python
    
    """
    return str(list(np.reshape(np.asarray(var), (1, np.size(var)))[0]))[1:-1]


def SortByState(tweets, word, state, abbrv, out):
    """Find all tweets that contain a keyword and they are tweeted from a certain state. 
    Caluclate average sentiment score.
    Write the result to output file in JSON format.

    Result format:
        'state_fullname': avg_sentiment_score
    
    Arguments:
        tweets {dataframe} -- dataframe of tweets
        word {string} -- keyword to check
        state {string} -- state fullname
        abbrv {string} -- state name abrreviation
        out {_io.TextIOWrapper} -- output file
    """     

    # find tweets that match the state
    tweets_in_state = tweets[tweets['user-location'].str.contains(state) | tweets['user-place-fullname'].str.contains(state) | (abbrv in tweets['user-location'].str.split(', ')) | (abbrv in tweets['user-place-fullname'].str.split(', '))]
    # calculate average sentiment score
    tweets_in_state_sentiment = analyzeSentiment(tweets_in_state, word)
    
    stringAv = to_str(tweets_in_state_sentiment)
    
    # write to file
    out.write("'")
    out.write(state)
    out.write("':")
    out.write(" ")
    print(state, abbrv)
    print(stringAv)
    print("-------")
    if stringAv == "nan":
        out.write("999")
    else:
        out.write(stringAv)
        
    if state != "D.C.":
        out.write(",\n")

    
def FormatDatetime(dt):
    """Format datetime string

    Format: YYYY-MM-DD HH:MM:SS
    
    Arguments:
        dt {string} -- datetime string
    
    Returns:
        string -- formatted datetime string
    """

    dt = dt.replace("_", " ")
    li = list(dt)
    li[13] = ":"
    li[16] = ":"
    return "".join(li)