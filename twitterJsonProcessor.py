import json

def readJson(filename):
	with open(filename, 'r') as myfile:
		data=myfile.read()
	tweets = json.loads(data)
	return processJson(tweets)
	
def processJson(tweets):
	read_tweets = {}
	for key in tweets.keys():
		map = {}
		map['text'] = tweets[key]['text']
		map['user'] = tweets[key]['user']['screen_name']
		read_tweets[key] = map
	return processText(read_tweets)

def processText(tweets):
	#further processing of text if necessary for better analysis
	return tweets

