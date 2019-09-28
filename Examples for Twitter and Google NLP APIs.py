#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tweepy #https://github.com/tweepy/tweepy
import json


#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


# In[29]:


#def get_all_tweets(screen_name):
    
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

all_tweet = []
tweets =  tweepy.Cursor(api.search,q='#DoubleTree' , count = 5, lang='en').items(10)
#file = open('tweets.json','w')
for tweet in tweets:
#    if 'text' in tweet._json:
#        print(tweet._json['text']) 
#        json.dump(tweet._json,file,sort_keys = True,indent = 4)
#print('Done')
#file.close()
        #all_tweet.append(tweet._json)
    dict_ = {'Screen Name': tweet.user.screen_name,
                'User Name': tweet.user.name,
                'Tweet Created At': tweet.created_at,
                'Tweet Text': tweet.text,
                'User Location': tweet.user.location,
                'Tweet Coordinates':tweet.coordinates,
                'Retweet Count': tweet.retweet_count,
                'Retweeted': tweet.retweeted,
                'Phone Type': tweet.source,
                'Favorite Count': tweet.favorite_count,
                'Favorited': tweet.favorited,
                'Replied': tweet.in_reply_to_status_id_str
                }
    all_tweet.append(dict_)   
print(all_tweet)


# In[30]:


import six
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
def analysis(text): 
    

    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    document = types.Document(
        content=text.encode('utf-8'),
        type=enums.Document.Type.PLAIN_TEXT)

    # Detect and send native Python encoding to receive correct word offsets.
    encoding = enums.EncodingType.UTF32
    if sys.maxunicode == 65535:
        encoding = enums.EncodingType.UTF16

    result = client.analyze_entity_sentiment(document, encoding)

    for entity in result.entities:
        print('Mentions: ')
        print(u'Name: "{}"'.format(entity.name))
        for mention in entity.mentions:
            print(u'  Begin Offset : {}'.format(mention.text.begin_offset))
            print(u'  Content : {}'.format(mention.text.content))
            print(u'  Magnitude : {}'.format(mention.sentiment.magnitude))
            print(u'  Sentiment : {}'.format(mention.sentiment.score))
            print(u'  Type : {}'.format(mention.type))
        print(u'Salience: {}'.format(entity.salience))
        print(u'Sentiment: {}\n'.format(entity.sentiment))


# In[31]:


for tweet in all_tweet:
    text = tweet['Tweet Text']
    analysis(text)


# In[ ]:




