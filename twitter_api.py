import datetime
import json
import sys
from os import path
from twitter_authenticateUser import auth_user
import tweepy




if(len(sys.argv) != 3):
	print("Please provide the twitter auth json and the user in that order")
if(not path.exists(sys.argv[1])):
	print("The supplied json file doest exist, please provide complete path")

def getFirstFiftyTweetsJson(twitter_json,twitter_handle_name):
	api = auth_user(twitter_json,twitter_handle_name);
	tweets =  tweepy.Cursor(api.search,q= twitter_handle_name, count = 5, lang='en').items(10)
	json_towrite = {}
	count = 0;
	for tweet in tweets:
		json_towrite[count] = tweet._json
		count += 1
	name = ('JsonFromTwitterFirstFifty'+str(datetime.datetime.now())+'.json').replace(" ","");
	twitterJsonFile = open(name,"w");
	twitterJsonFile.write(json.dumps(json_towrite, indent=4))
	return json_towrite


getFirstFiftyTweetsJson(sys.argv[1],sys.argv[2])



