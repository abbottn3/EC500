import json
from pymongo import MongoClient
import pprint
dbclient = MongoClient()
db = dbclient.Twitter_Info

input_user = raw_input("Enter a Twitter handle to see trends: ")
user = db[input_user]
entities = []
labels = []
texts = 0
for post in user.find():

	entities.append(post['entity'])
	entities.append(post['label'])
	if (post['text'] == 'true'):
		texts += 1
if (len(entities) > 0):
	print('The recent topics of posts from this account are: '),
	for item in list(set(entities)):
		print(item + ', '),
else:
	print('Error: no info logged for that username')