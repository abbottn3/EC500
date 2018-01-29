# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 20:46:02 2018

@author: Noah Abbott
"""

import tweepy
import json
import sys
import wget

# OAuth Keys/Secrets
consumer_key = "xauVSLqGqtLqc593XJwuMrl9r"
consumer_secret = "as9WhJtrr5Y47iag4sBgUYyBJBmwxvMon3GLL8oJK6sMwpmVDF"
access_token = "874676070636814338-OmsqKer9vLzEOkvOJkDcdob9emKZn89"
access_token_secret = "eCMWhQg5JgeIoV7TJAvW0RdmNOYlUbMSNkqTZjmu7epEn"
user_handle = "abbottn3"

# OAuth Attempt
try:    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
except tweepy.TweepError:
    print ("Error -- keys/secrets are incompatible")
    sys.exit()

# Verifying Twitter Handle
try:
    user = api.get_user(user_handle)
except tweepy.TweepError:
    print ("Error -- invalid Twitter handle")
    sys.exit()


print (user.screen_name)
print (user.followers_count)
for friend in user.friends():
   print (friend.screen_name)
   
tweets = api.home_timeline(screen_name = user_handle, count = 100)
#print json.dumps([status._json for status in tweets])

media_files = set()
for status in tweets:
    media = status.entities.get('media', [])
    if len(media) > 0:
        media_files.add(media[0]['media_url'])
    if len(media_files) >= 5:
    	break

print '\n\n'
print media_files

#for media_file in media_files:
#    wget.download(media_file)

