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
OAuthFilePath = 'C:/Users/abbot/Desktop/Everything/College/Building_Software/API_Exercise/pyOAuth.txt'
with open(OAuthFilePath) as fp:
    consumer_key = fp.readline().rstrip('\n')
    consumer_secret = fp.readline().rstrip('\n')
    access_token = fp.readline().rstrip('\n')
    access_token_secret = fp.readline().rstrip('\n')


user_handle = "abbottn3"
print consumer_key
#print '\n'
print consumer_secret
#print '\n'
print access_token
#print '\n'
print access_token_secret
#print '\n'

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


print ('Grabbing images from ' + user.screen_name)
   
tweets = api.user_timeline(screen_name = user_handle, count = 100)
#print json.dumps([status._json for status in tweets])

media_files = set()
for status in tweets:
    media = status.entities.get('media', [])
    if len(media) > 0:
        media_files.add(media[0]['media_url'])
    if len(media_files) >= 5:
    	break
if len(media_files) <= 5:
    print ('Only ' + str(len(media_files)) + ' images in last 100 posts')
#could add question to continue here

print media_files

for media_file in media_files:
    wget.download(media_file)

