# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 2018

@author: Noah Abbott
"""

import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
'''
googlecredstxt = open('googlecreds.txt','r')
googlecreds = googlecredstxt.read()
googlecredstxt.close()
'''
# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'Adam.JPG')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations


print('Labels:')
for label in labels:
    print(label.description)

webnotes = response.web_detection
if webnotes.web_entities:
	if webnotes.web_entities[0].score > 1:
		print('Description: {}'.format(webnotes.web_entities[0].description))
	else:
		print('Score      : {}'.format(entity.score))
        print('Description: {}'.format(entity.description))