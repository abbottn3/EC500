# -*- coding: utf-8 -*-
"""
Created on Sun Feb 4 2018

@author: Noah Abbott
"""
# Imports tweepy
import tweepy
import json
import sys
import wget

import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# OAuth Keys/Secrets
OAuthFilePath = 'C:/Users/abbot/Desktop/Everything/College/Building_Software/API_Exercise/pyOAuth.txt'
with open(OAuthFilePath) as fp:
    consumer_key = fp.readline().rstrip('\n')
    consumer_secret = fp.readline().rstrip('\n')
    access_token = fp.readline().rstrip('\n')
    access_token_secret = fp.readline().rstrip('\n')

# OAuth Attempt
try:    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
except tweepy.TweepError:
    print ("Error -- keys/secrets are incompatible")
    sys.exit()

# Request Twitter Handle
user_handle = raw_input("Enter a Twitter handle: ")

# Verifying Twitter Handle
try:
    user = api.get_user(user_handle)
except tweepy.TweepError:
    print ("Error -- invalid Twitter handle")
    sys.exit()

# Grab last *count* images from *screen_name*
print ('Grabbing images from ' + user.screen_name + '...')
tweets = api.user_timeline(screen_name = user_handle, count = 100)

# Makes list of image URLs
media_files = set()
for status in tweets:
    media = status.entities.get('media', [])
    if len(media) > 0:
        media_files.add(media[0]['media_url'])
    if len(media_files) >= 5:
    	break
if 0 < len(media_files) < 5:
    print ('Only ' + str(len(media_files)) + ' images in last 100 posts')
# note: could add question her to continue or not
if len(media_files) == 0:
	print("Error -- No images in last 100 posts")
	sys.exit()

# Download image (for testing)
for mf1 in media_files:
	break
wget.download(mf1)


# Instantiates a client for Google Vision
client = vision.ImageAnnotatorClient()

'''
# To read local picture
file_name = os.path.join(
    os.path.dirname(__file__),
    'Adam.JPG')

with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)
'''

# To read pic from url
image = types.Image()
image.source.image_uri = mf1;


# Checking for logos
response = client.logo_detection(image=image)
logos = response.logo_annotations
if logos:
	print('Description: {}'.format(logos.description))

# Checking for web entities
response = client.web_detection(image=image)
webnotes = response.web_detection
webEnts = set()
cnt = 0
if webnotes.web_entities:
	for entity in webnotes.web_entities:
		if entity.score > 1:
			print('Description: {}'.format(entity.description))
			cnt += 1;

# If no web entities, use labels
if cnt == 0:
	# Performs label detection on the image file
	response = client.label_detection(image=image)
	labels = response.label_annotations
	for i in range(0,3):
		print('Description: {}'.format(labels[i].description))
