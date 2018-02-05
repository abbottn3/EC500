# -*- coding: utf-8 -*-
"""
Created on Sun Feb 4 2018

@author: Noah Abbott
"""
# Imports tweepy
import tweepy
import ffmpy
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

'''
# Download image (for testing)
for mf1 in media_files:
	break
wget.download(mf1)
'''

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
filecnt = 1
files2delete = []
fnames = open('filenames.txt', 'w')
picdescripts = open('SSdescriptions.txt', 'w')
picdescripts.write('Summary Slideshow Descriptions\n')

for mf1 in media_files:
	kind = 0
	DLpic = wget.download(mf1);
	files2delete.append(DLpic)
	ff = ffmpy.FFmpeg(
		inputs={DLpic: '-loop 1'},
		outputs={'file' + str(filecnt) + '.mp4': ['-y', '-c:a', 'libfdk_aac', '-ar', '44100', '-ac', '2', '-vf', "scale='if(gt(a,16/9),1280,-1)':'if(gt(a,16/9),-1,720)', pad=1280:720:(ow-iw)/2:(oh-ih)/2", '-c:v', 'libx264', '-b:v', '10M', '-pix_fmt', 'yuv420p', '-r', '30', '-shortest', '-avoid_negative_ts', 'make_zero', '-fflags', '+genpts', '-t', '2']}
		)
	ff.run()
	fnames.write("file 'file" + str(filecnt) + ".mp4'\n")
	files2delete.append('file' + str(filecnt) + '.mp4')
	
	
	# To read pic from url
	picdescripts.write("\nImage {}: ".format(filecnt))
	image = types.Image()
	image.source.image_uri = mf1;
	filecnt += 1

	# Checking for labels
	response = client.label_detection(image=image)
	labels = response.label_annotations
	if labels:
		if str(labels[0].description) == 'text':
			kind = 'text'
			picdescripts.write('its a text document')

	# Checking for logos
	response = client.logo_detection(image=image)
	logos = response.logo_annotations
	if logos:
		picdescripts.write('Logo Description: {}'.format(logos[0].description))
		kind = 'logo'

	# Checking for web entities
	if kind == 'text':
		escore = 1
	else:
		escore = 2
	response = client.web_detection(image=image)
	webnotes = response.web_detection
	webEnts = set()
	cnt = 0
	if webnotes.web_entities:
		if webnotes.web_entities[0] > escore:
			picdescripts.write('Web Description: {}'.format(webnotes.web_entities[0].description))
			cnt += 1
		for entity in webnotes.web_entities:
			if entity.score > escore:
				if entity == webnotes.web_entities[0]:
					continue
				picdescripts.write(', {}'.format(entity.description))
				

	# If no web entities, use labels
	if cnt == 0:
		response = client.label_detection(image=image)
		labels = response.label_annotations
		if labels:
			picdescripts.write('Label Description: {}, {}'.format(labels[0].description, labels[1].description))

fnames.close()
picdescripts.close()
ff2 = ffmpy.FFmpeg(
	inputs={'filenames.txt': '-f concat'},
	outputs={'SummarySlideshow.mp4': '-y'}
	)
ff2.run()

# Delete Leftover Files
files2delete.append('filenames.txt')
for delfile in files2delete:
	os.remove(delfile)