#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tweepy #https://github.com/tweepy/tweepy
import json

from google.cloud import language_v1
from google.cloud.language_v1 import enums
import six

import sys
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


# In[2]:


# Get tweets
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

all_tweet = []
tweets =  tweepy.Cursor(api.search,q='@foston_q' , count = 5, lang='en').items(10)

for tweet in tweets:
    dict_ = {
                'User Name': tweet.user.name,
                'Tweet Text': tweet.text,
                }
    all_tweet.append(dict_) 
new_file = open('validdata.json','w')
json.dump(all_tweet, new_file,sort_keys = True,indent = 4)
new_file.close()
print(all_tweet)


# In[3]:


# Google NLP

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


# Analyze text
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


# In[5]:


result = []
for tweet in all_tweet:
    result.append(sample_analyze_sentiment(tweet['User Name'], tweet['Tweet Text']))

file = open('Analysis_Result.json', 'w')
json.dump(result, file, indent = 4)
file.close()


# In[ ]:


import pandas as pd
df = pd.DataFrame(result)
df


# In[ ]:


# Sort the complians according to the sentiment score
df = df.sort_values(by=['Score','Magnitude'])
df = df.reset_index().drop('index',axis = 1)
df


# In[60]:


# identify the department

safe_dp = ['safe','dangerous', 'scared','terrifying']
cleaness_dp=['clean','dirty','mass','miry','mucky']
peak_dp=['busy','crowded','lot of people','rush','heavy traffic','peak']

pd.set_option('mode.chained_assignment', None)
df['Department'] = 'General'

for x in df.index:
    if(any(keyword in df['Content'][x] for keyword in safe_dp)):
        df['Department'][x] = 'Safety'
    elif(any(keyword in df['Content'][x] for keyword in cleaness_dp)):
        df['Department'][x] = 'Cleaness'
    elif(any(keyword in df['Content'][x] for keyword in peak_dp)):
        df['Department'][x] = 'Peak Hour'
    else: 
        df['Department'][x] = 'General'
df


# In[63]:


# Trigger the email
import smtplib, ssl
# coding=utf-8
def sendemail(sender, receiver, username, content, department):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = sender  # Enter your address
    receiver_email = receiver  # Enter receiver address
    password = input("Type your password and press enter: ")
    message = """    Subject: Gravience from twitter

    """ + "To " + department + " Department:" + "\n" + content + "\n" + "From " + username

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


# In[64]:


string = str(df['Content'][0]).encode("ascii", "ignore").decode('utf-8')

sendemail("373881462h@gmail.com","373881462h@gmail.com", df['User Name'][0], string, df['Department'][0])






