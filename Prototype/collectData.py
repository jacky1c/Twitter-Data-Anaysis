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

import datetime
import json
import glob
from pprint import pprint
from functions import * # self defined functions


# File to save Twitter data
currentDT = datetime.now()
timeStr = currentDT.strftime("%Y-%m-%d_%H:%M:%S")
n = 1000

# Set keywords
Trump = ('Trump')
Pelosi = ('Pelosi')
Sotu = ('State of the Union', 'sotu')

# Set filenames
TrumpFilename = 'Trump_'+timeStr+'.json'
PelosiFilename = 'Pelosi_'+timeStr+'.json'
SotuFilename = 'SOTU_'+timeStr+'.json'

# Collect 1000 tweets from Twitter API and export to json file
collect_twitter_data(Trump, n, TrumpFilename)  
collect_twitter_data(Pelosi, n, PelosiFilename)
collect_twitter_data(Sotu, n, SotuFilename)

