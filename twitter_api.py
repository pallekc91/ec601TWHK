import datetime
import json
import sys
from os import path
from twitter_authenticateUser import auth_user
import tweepy


def getFirstFiftyTweetsJson(twitter_json,twitter_handle_name):
	api = auth_user(twitter_json,twitter_handle_name);
	tweets =  tweepy.Cursor(api.search,q= twitter_handle_name, count = 5, lang='en').items(10)
	return write_json(tweets)

def getTweetsFromTheDay(twitter_json,twitter_handle_name,start_MMDDYY):
	api = auth_user(twitter_json,twitter_handle_name);
	start_date = datetime.datetime(2000+int(start_MMDDYY[4:6]), int(start_MMDDYY[0:2]), int(start_MMDDYY[2:4]), 12, 00, 00)
	end_date = datetime.datetime(2000+int(start_MMDDYY[4:6]), int(start_MMDDYY[0:2])+1, int(start_MMDDYY[2:4]), 12, 00, 00)
	tweets = tweepy.Cursor(api.user_timeline, screen_name=twitter_handle_name, since=start_date, until=end_date).items()
	return write_json(tweets)

def getMentions(twitter_json,twitter_handle_name,search_terms,start_MMDDYY):
	api = auth_user(twitter_json,twitter_handle_name);
	start_date = datetime.datetime(2000+int(start_MMDDYY[4:6]), int(start_MMDDYY[0:2]), int(start_MMDDYY[2:4]), 12, 00, 00)
	end_date = datetime.datetime(2000+int(start_MMDDYY[4:6]), int(start_MMDDYY[0:2]), int(start_MMDDYY[2:4])+1, 12, 00, 00)
	#tweets = tweepy.Cursor(api.mentions_timeline,since=start_date,until=end_date,ang="en").items()
	#tweets = tweepy.Cursor(api.search, q=search_terms).items()
	tweets = tweepy.Cursor(api.search,
              q=search_terms,
              lang="en",
              since=start_date,
              until=end_date).items(50)
	return write_json(tweets)

def write_json(tweets):
	json_towrite = {}
	count = 0;
	for tweet in tweets:
		json_towrite[count] = tweet._json
		count += 1
	name = ('JsonFromTwitter'+str(datetime.datetime.now())+'.json').replace(" ","");
	twitterJsonFile = open(name,"w");
	twitterJsonFile.write(json.dumps(json_towrite, indent=4))
	return name



