

def readJson(filename):
	with open(filename, 'r') as myfile:
		data=myfile.read()
	tweets = json.loads(data)
	processJson(tweets)
	
def processJson(tweets):
	read_tweets = {}
	for key in tweets.keys():
		read_tweets[key] = tweets[key]['text']
	return processText(read_tweets)

def processText(tweets):
	#further processing of text if necessary for better analysis
	return tweets

