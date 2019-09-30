import tweepy
import argparse
import sys
import json
from os import path

if(len(sys.argv) != 3):
	print("Please provide the twitter auth json and the user in that order")
if(not path.exists(sys.argv[1])):
	print("The supplied json file doest exist, please provide complete path")

def auth_user(twitter_json,twitter_handle_name):
    with open(twitter_json) as json_file:
        twitterAuth = json.load(json_file)
    auth = tweepy.OAuthHandler(twitterAuth["consumer_key"],twitterAuth["consumer_secret"])
    auth.set_access_token(twitterAuth["access_token_key"],twitterAuth["access_token_secret"])
    api = tweepy.API(auth)
    try:
        user = api.get_user(twitter_handle_name)
    except Exception:
        print("User "+ twitter_handle_name +" doesnt exist")
    return api

auth_user(sys.argv[1],sys.argv[2])
