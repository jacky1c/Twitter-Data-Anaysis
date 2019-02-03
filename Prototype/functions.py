#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 13:14:44 2019

@author: jacky
"""
import json
import tweepy
from tweepy.streaming import StreamListener
from slistener import SListener

def collect_twitter_data(outfilename):
    """ Collect data through Twitter API and export to JSON file. """
    # =============================================================================
    # CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, and ACCESS_SECRET are assigned by Twitter
    # =============================================================================

    # Consumer key authentication
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    # Access key authentication
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    
    # Set up the API with the authentication handler
    api = tweepy.API(auth)
    
    # Instantiate the SListener object
    listen = SListener(api)
    
    # Instantiate the Stream object
    stream = tweepy.Stream(auth, listen)
    
    # Set up words to track
    keywords_to_track = ('super bowl', 'superbowl')
    
    # Begin collecting data
    tweet_data = tweepy.Cursor(api.search, q=keywords_to_track, languages=["en"]).items(1000)
    
    # Export tweets to file
    ctr = 0
    with open(outfilename,'w') as outfile:
        outfile.write('[')
        for twit in tweet_data:
            ctr = ctr+1
            json.dump(twit._json, outfile)
            if ctr != 1000:
                outfile.write(',')
        outfile.write(']')   
        

def flatten_tweets(tweets_dict_list):
    """ Flattens out tweet dictionaries so relevant JSON is in a top-level dictionary. """
    tweets_list = []
    
    # Iterate through each tweet
    for tweet_obj in tweets_dict_list:
    
        # Store the user screen name in 'user-screen_name'
        tweet_obj['user-screen_name'] = tweet_obj['user']['screen_name']
    
        # Check if this is a 140+ character tweet
        if 'extended_tweet' in tweet_obj:
            # Store the extended tweet text in 'extended_tweet-full_text'
            #tweet_obj['extended_tweet-full_text'] = tweet_obj['extended_tweet']['full_text']
            tweet_obj['text'] = tweet_obj['text'] + tweet_obj['extended_tweet']['full_text']
    
        if 'retweeted_status' in tweet_obj:
            # Store the retweet user screen name in 'retweeted_status-user-screen_name'
            tweet_obj['retweeted_status-user-screen_name'] = tweet_obj['retweeted_status']['user']['screen_name']
            # Store the retweet text in 'retweeted_status-text'
            tweet_obj['retweeted_status-text'] = tweet_obj['retweeted_status']['text']
            if 'extended_tweet' in tweet_obj['retweeted_status']:
                tweet_obj['retweeted_status-text'] = tweet_obj['retweeted_status-text'] + tweet_obj['retweeted_status']['extended_tweet']['full_text']
            
        if 'quoted_status' in tweet_obj:
            tweet_obj['quoted_status-text'] = tweet_obj['quoted_status']['text'] 
            if 'extended_tweet' in tweet_obj['quoted_status']:
                tweet_obj['quoted_status-text'] = tweet_obj['quoted_status-text'] + tweet_obj['quoted_status']['extended_tweet']['full_text']
            
        tweets_list.append(tweet_obj)
    return tweets_list

def check_word_in_tweet(word, data):
    """Checks if a word is in a Twitter dataset's text. 
    Checks text and extended tweet (140+ character tweets) for tweets,
    retweets and quoted tweets.
    Returns a logical pandas Series.
    """
    contains_column = data['text'].str.contains(word, case = False)
    #contains_column |= data['extended_tweet-full_text'].str.contains(word, case = False)
    contains_column |= data['quoted_status-text'].str.contains(word, case = False)
    #contains_column |= data['quoted_status-extended_tweet-full_text'].str.contains(word, case = False)
    contains_column |= data['retweeted_status-text'].str.contains(word, case = False)
    #contains_column |= data['retweeted_status-extended_tweet-full_text'].str.contains(word, case = False)
    return contains_column