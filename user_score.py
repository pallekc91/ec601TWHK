import tweepy
import json
from google_api import *
from twitterJsonProcessor import *
from twitter_api import *
from twitter_authenticateUser import *

def getUserScore(twitter_json,user_twitter_handle):
	api = auth_user(twitter_json,user_twitter_handle);
	tweets =  tweepy.Cursor(api.search,q= user_twitter_handle, count = 5, lang='en').items(10)
	json_towrite = {}
	count = 0;
	for tweet in tweets:
		json_towrite[count] = tweet._json
		count += 1
	processed_tweets = processJson(json_towrite)
	score = 0
	for key in processed_tweets.keys():
		score += float(analysis(processed_tweets[key])['Sentiment'])
	return score/len(processed_tweets.keys())

print(getUserScore(sys.argv[1],sys.argv[2]))