from twitter_api import getTweetsFromTheDay,getMentions
from twitterJsonProcessor import readJson
from google_api import analysis_json
from user_score import addUserScore
from identifyDepartment import identifyDepartment
import sys
from datetime import date,timedelta

def run(twitter_cre):
	#prev_date = (date.today()).strftime('%m%d%y')
	prev_date = '092619'
	#search_terms = ['foston_q','@foston_q','.@foston_q','. @foston_q']
	search_terms = '@foston_q'
	twitter_json_name = getMentions(twitter_cre,'foston_q',search_terms,prev_date)
	#twitter_json_name = getTweetsFromTheDay(twitter_cre,'foston_q',prev_date)
	processed_tweets = readJson(twitter_json_name)
	addUserScore(twitter_cre,processed_tweets)
	identifyDepartment(processed_tweets)
	google_json_name = analysis_json(processed_tweets)
	print(processed_tweets)


run(sys.argv[1])


