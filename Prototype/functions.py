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
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt  
import numpy as np   

def collect_twitter_data(outfilename):
    """ Collect data through Twitter API and export to JSON file. """
    # =============================================================================
    # CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, and ACCESS_SECRET are assigned by Twitter
    # =============================================================================
    
    # Twitter App access keys for @user

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
    
    # Set up words to track
    keywords_to_track = ('State of the Union', 'sotu')
    
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
        tweet_obj['created_at'] =  pd.to_datetime(tweet_obj['created_at'])
        
        #store the location
        tweet_obj['user-location'] = tweet_obj['user']['location']
        


        
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
            tweet_obj['retweet-location'] = tweet_obj['retweeted_status']['user']['location']
            if 'extended_tweet' in tweet_obj['retweeted_status']:
                tweet_obj['retweeted_status-text'] = tweet_obj['retweeted_status-text'] + tweet_obj['retweeted_status']['extended_tweet']['full_text']
            
        if 'quoted_status' in tweet_obj:
            tweet_obj['quoted_status-text'] = tweet_obj['quoted_status']['text'] 
            tweet_obj['quoted-location'] = tweet_obj['quoted_status']['user']['location']
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

def plotMapTime(ds_tweets, word1, word2):
    

    ds_tweets['word1'] = check_word_in_tweet(word1, ds_tweets)
    ds_tweets['word2'] = check_word_in_tweet(word2, ds_tweets)

    ds_tweets['word1'].index = pd.to_datetime(ds_tweets.index, unit='s')
    ds_tweets['word2'].index = pd.to_datetime(ds_tweets.index, unit='s')


    mean1 = ds_tweets['word1'].resample('1 min').mean()
    mean2 = ds_tweets['word2'].resample('1 min').mean()



    plt.plot(mean1.index.minute, mean1, color = 'green')
    plt.plot(mean2.index.minute, mean2, color = 'blue')


    plt.xlabel('Minute'); plt.ylabel('Frequency')
    plt.title('Language mentions over time')
    plt.legend((word1, word2))
    plt.show()





def analyzeSentiment(ds_tweets, word):
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
    
    sid = SentimentIntensityAnalyzer()

    # Generate sentiment scores by applying polarity_scores function to all tweet text
    sentiment_scores = ds_tweets['text'].apply(sid.polarity_scores)

    # Extract compound from sentiment score. Options are: neg, neu, pos, compound
    sentiment = sentiment_scores.apply(lambda x: x['compound'])
    
    

    ds_tweets['word1'] = sentiment[check_word_in_tweet(word1, ds_tweets)]
    
    ds_tweets['word1'].index = pd.to_datetime(ds_tweets.index, unit='s')
    
    
    sentiment1 = ds_tweets['word1'].resample('1 min').mean()
    
    
    
    
    
    ds_tweets['word2'] = sentiment[check_word_in_tweet(word2, ds_tweets)]
    
    ds_tweets['word2'].index = pd.to_datetime(ds_tweets.index, unit='s')
    
    
    sentiment2 = ds_tweets['word2'].resample('1 min').mean()
    
    
  
    
    

#
    plt.plot(sentiment1.index.minute, sentiment1, color = 'green')
    plt.plot(sentiment2.index.minute, sentiment2, color = 'blue')

    plt.xlabel('Minute')
    plt.ylabel('Sentiment')
    plt.title('Sentiment of data science languages')
    plt.legend((word1, word2))
    plt.show()

    
    




def SortByState(tweets):
    
#    tweets.index = tweets['user-location']
#    
#    tweets['currentState'] = "Alabama"
#    
#    hold = tweets.apply(lambda x: x['currentState'] in x['user-location'], axis=1)
#    
#    containsAL1 = tweets[tweets['user-location'].str.contains("TX")==True]
#    
#    #hold = tweets[tweets['user-location'].str.contains("AL")]
#    containsAL2 = tweets[tweets['user-location'].str.contains(" AL")]
#
#    print(hold)
#    print(np.sum(hold))
   # print(containsAL1['user-location'])

    
#    test = tweets[tweets['user-location'].str.contains(" TX", case = False)]
#    test |= tweets[tweets['retweet-location'].str.contains(" TX", case = False)]
#    test |= tweets[tweets['quoted-location'].str.contains(" TX", case = False)]
#    print(np.sum(test))
#    
    
#    test = tweets[tweets['user-location'].str.contains(" TX", case = False)]
#    test |= tweets['retweet-location'].str.contains(" TX", case = False)
#    test |= tweets['quoted-location'].str.contains(" TX", case = False)
#    print(np.sum(test))
    
    
    containsAL1 = tweets[tweets['user-location'].str.contains("Texas")==True]
    containsALR = tweets[tweets['retweet-location'].str.contains("Texas")==True]
    containsALQ = tweets[tweets['quoted-location'].str.contains("Texas")==True]
    #print(np.sum(containsAL1))
    
    print("Normal")
    
    print(containsAL1['text'])
    
    print("Retweet")
    print(containsALR['text'])
    
    print("Quoted")
    print(containsALR['text'])
    
    
