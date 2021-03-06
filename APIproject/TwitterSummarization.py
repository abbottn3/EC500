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
import datetime

import io
import os

import sys
reload(sys)
sys.setdefaultencoding('utf8')

# For MongoDB
from pymongo import MongoClient

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Global variable for list of files to delete
files2delete = []

# Receives twitter handle, returns list of image URLs
def twitterDL(user_handle):
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
	return media_files

# Receives list of image URLs, returns dictionary of descriptions 
def gVision_and_FFMPEG(mFiles, t_handle):
	# Instantiates a client for Google Vision
	client = vision.ImageAnnotatorClient()

	# Creating files for writing
	fnames = open('filenames.txt', 'w')
	files2delete.append('filenames.txt')
	picdescripts = open('SSdescriptions.txt', 'w')
	picdescripts.write('Summary Slideshow Descriptions\n')
	#asdofiaf
	filecnt = 0

	# To run for each image url in media_files
	for mf1 in mFiles:
		# Create dictionary for MongoDB
		db_dict = {}
		db_dict['name'] = 'Image_{}'.format(filecnt)
		db_dict['date'] = datetime.datetime.utcnow()

		# Temporarily download image and add to "to delete" list
		pictype = 0
		DLpic = wget.download(mf1);
		files2delete.append(DLpic)

		# FFMPEG turns image into mp4
		ff = ffmpy.FFmpeg(
			inputs={DLpic: '-loop 1'},
			outputs={'file' + str(filecnt) + '.mp4': ['-y', '-c:a', 'libfdk_aac', '-ar', '44100', '-ac', '2',
			'-vf', "scale='if(gt(a,16/9),1280,-1)':'if(gt(a,16/9),-1,720)', pad=1280:720:(ow-iw)/2:(oh-ih)/2",
			'-c:v', 'libx264', '-b:v', '10M', '-pix_fmt', 'yuv420p', '-r', '30', '-shortest',
			'-avoid_negative_ts', 'make_zero', '-fflags', '+genpts', '-t', '2']}
			)
		ff.run()
		fnames.write("file 'file" + str(filecnt) + ".mp4'\n")
		files2delete.append('file' + str(filecnt) + '.mp4')
		
		
		# Read picture from url
		picdescripts.write("\nImage {}: ".format(filecnt+1))
		image = types.Image()
		image.source.image_uri = mf1
		

		# Checking if it's just a text file (with labels)
		response = client.label_detection(image=image)
		labels = response.label_annotations
		if labels:
			if str(labels[0].description) == 'text':
				pictype += 1
				picdescripts.write('Text document about: ')
				db_dict['text'] = 'true'
			else:
				db_dict['text'] = 'false'


		# Checking for logos
		response = client.logo_detection(image=image)
		logos = response.logo_annotations
		if logos:
			db_dict['logo'] = logos[0].description
			if pictype > 0:
				picdescripts.write(logos[0].description)
			else:
				picdescripts.write('Logo Description: {}, '.format(logos[0].description))
				pictype += 1

		# Checking for web entities. Note: if it's a text file or has a logo, we can be less picky with the
		# web description, and therefore set the minimum matching score 'escore' to 1. Else, set to 2.
		# Additionally, if it's a text doc or has a logo, the formatting is different, hense the if/else statements.
		if pictype > 0:
			escore = 1
		else:
			escore = 3
		response = client.web_detection(image=image)
		webnotes = response.web_detection
		webEnts = set()
		cnt = 0
		if webnotes.web_entities:
			if webnotes.web_entities[0] > escore:
				db_dict['entity'] = webnotes.web_entities[0].description
				if pictype > 0:
					picdescripts.write(webnotes.web_entities[0].description)
				else:
					picdescripts.write('Web Description: {}'.format(webnotes.web_entities[0].description))
				cnt += 1
			for entity in webnotes.web_entities:
				if entity.score > escore:
					if entity == webnotes.web_entities[0]:
						continue
					picdescripts.write(', {}'.format(entity.description))
					

		# If no web entities, use labels
		response = client.label_detection(image=image)
		labels = response.label_annotations

		if labels:
			if pictype > 0:
				db_dict['label'] = labels[1].description
				if cnt ==0:
					picdescripts.write(labels[1].description)
				else:
					picdescripts.write(', {}'.format(labels[1].description))
			else:
				db_dict['label'] = labels[0].description
				if cnt == 0:
					picdescripts.write('Label Description: {}, {}'.format(labels[0].description, labels[1].description))
				else:
					picdescripts.write(', {}'.format(labels[0].description))
		filecnt += 1
		# Inserting into MongoDB
		ins_MongoDB(t_handle, db_dict)

	# Close the files and compile the slideshow
	fnames.close()
	picdescripts.close()
	ff2 = ffmpy.FFmpeg(
		inputs={'filenames.txt': '-f concat'},
		outputs={'SummarySlideshow.mp4': '-y'}
		)
	ff2.run()
	return db_dict

def ins_MongoDB(t_handle, db_dict):
	dbclient = MongoClient()
	dbname = 'Twitter_Info'
	db = dbclient[dbname]
	user_info = db[t_handle]
	#parsed = json.dumps(description_dict)
	#for image in description_dict:
	user_info.insert_one(db_dict)



def get_files():
	return files2delete

def main():

	# Request Twitter Handle
	t_handle = raw_input("Enter a Twitter handle: ")

	# Grabs pic URLs
	pic_urls = twitterDL(t_handle)

	# Returns dictionary of applicable descriptions
	if len(pic_urls) != 0:
		description_dict = gVision_and_FFMPEG(pic_urls, t_handle)


	# Delete leftover files
	for delfile in files2delete:
		os.remove(delfile)

if __name__ == "__main__":
    main()