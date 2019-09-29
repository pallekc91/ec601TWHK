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


# In[2]:


#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

all_tweet = []
tweets =  tweepy.Cursor(api.search,q='@foston_q' , count = 5, lang='en').items(10)

# Save tweets in json file 
#file = open('tweets.json','w')
#for tweet in tweets:
#    if 'text' in tweet._json:
#       print(tweet._json['text'] + '\n') 
#       json.dump(tweet._json,file,sort_keys = True,indent = 4)
#print('Done')
#file.close()
#all_tweet.append(tweet._json)

for tweet in tweets:
    dict_ = {#'Screen Name': tweet.user.screen_name,
                'User Name': tweet.user.name,
                #'Tweet Created At': tweet.created_at,
                'Tweet Text': tweet.text,
               # 'User Location': tweet.user.location,
              #  'Tweet Coordinates':tweet.coordinates,
               # 'Retweet Count': tweet.retweet_count,
               #'Retweeted': tweet.retweeted,
                #'Phone Type': tweet.source,
               # 'Favorite Count': tweet.favorite_count,
               # 'Favorited': tweet.favorited,
              #  'Replied': tweet.in_reply_to_status_id_str
                }
    all_tweet.append(dict_) 
new_file = open('validdata.json','w')
json.dump(all_tweet, new_file,sort_keys = True,indent = 4)
new_file.close()
print(all_tweet)


# In[3]:


from google.cloud import language_v1
from google.cloud.language_v1 import enums
import six

def sample_analyze_sentiment(username, content):

    client = language_v1.LanguageServiceClient()

    #content = 'Your text to analyze, e.g. Hello, world!'

    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': content}

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment
    print('User Name: {}'.format(username))
    print('Content: {}'.format(content))
    print('Score: {}'.format(sentiment.score))
    print('Magnitude: {}'.format(sentiment.magnitude)+ '\n')
    
    dict_ = {
        'User Name': username,
        'Content': content,
        'Score': sentiment.score,
        'Magnitude': sentiment.magnitude
    }
    
    return dict_
    
#sample_analyze_sentiment('Hello World'))


# In[4]:


import sys
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
        print(u' Name: "{}"'.format(entity.name))
        for mention in entity.mentions:
            print(u'  Begin Offset : {}'.format(mention.text.begin_offset))
            print(u'  Content : {}'.format(mention.text.content))
            print(u'  Magnitude : {}'.format(mention.sentiment.magnitude))
            print(u'  Sentiment : {}'.format(mention.sentiment.score))
            print(u'  Type : {}'.format(mention.type))
        print(u'Salience: {}'.format(entity.salience))
        print(u'Sentiment: {}\n'.format(entity.sentiment))


# In[ ]:





# In[5]:


result = []
for tweet in all_tweet:
    result.append(sample_analyze_sentiment(tweet['User Name'], tweet['Tweet Text']))

file = open('Analysis_Result.json', 'w')
json.dump(result, file, indent = 4)
file.close()


# In[6]:


import pandas as pd
df = pd.DataFrame(result)
df


# In[7]:


df = df.sort_values(by=['Score','Magnitude'])
df = df.reset_index().drop('index',axis = 1)
df


# In[8]:


import smtplib, ssl
# coding=utf-8
def sendemail(sender, receiver, username, content):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = sender  # Enter your address
    receiver_email = receiver  # Enter receiver address
    password = input("Type your password and press enter: ")
    message = """    Subject: Gravience from twitter

    """ + "\n" + content + "\n" + "From " + username

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


# In[9]:


string = str(df['Content'][0]).encode("ascii", "ignore").decode('utf-8')

sendemail("Type sender email address here","Type reciever email address here", df['User Name'][0], string)


# In[ ]:





# In[ ]:




