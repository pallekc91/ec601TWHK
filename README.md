# Build a Sentiment Analysis System for for the Metro Rail Transportation system
This is a basic structure on how to build a sentiment anylysis for the Metro Rail Transportation System.
## Preparation
* Twitter API
* Google NLP
### Get Twitter API keys
To start with, you will need to have a Twitter developer account and obtain credentials (i.e. API key, API secret, Access token and Access token secret) on the to access the Twitter API, following these steps:

* Create a Twitter developer account if you do not already have one from : https://developer.twitter.com/
* Go to https://developer.twitter.com/en/apps and log in with your Twitter user account.
* Click “Create an app”
* Fill out the form, and click “Create”
* A pop up window will appear for reviewing Developer Terms. Click the “Create” button again.
* In the next page, click on “Keys and Access Tokens” tab, and copy your “API key” and “API secret” from the Consumer API keys section.
* Scroll down to Access token & access token secret section and click “Create”. Then copy your “Access token” and “Access token secret”.

### Install Twitter Library
We will be using a Python library called Tweepy to connect to Twitter API and downloading the data from Twitter. There are many other libraries in various programming languages that let you use Twitter API. We choose the Tweepy for this tutorial, because it is simple to use yet fully supports the Twitter API.

Install tweepy by using pip/easy_install to pull it from PyPI:
`$ pip install tweepy`
You may also use Git to clone the repository from GitHub and install it manually:

`$ git clone https://github.com/tweepy/tweepy.git
$ cd tweepy
$ python setup.py install`

### Get Google NLP ready
To get started with the Cloud Natural Language API using the Google Cloud SDK, see: https://cloud.google.com/natural-language/docs/quickstart for reference. 

---

## Collect tweets using Search API
To get the tweets that include the keyword you are searching for, copy the following code. For our system, we collected the tweets tagged **foston_q** which is an account that people can post their complains about transportation in Boston.
```python
tweets =  tweepy.Cursor(api.search,q='@foston_q' , count = 5, lang='en').items(10)
```
## Save data into JSON file
After that, we store the tweet text and user name into a JSON file, you could find **validdata.json** in the *same path* with .py file. 
```python 
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
```
## Google sentiment analysis
Once we obtain the data from twitter, we could process the google sentiment analysis. Here's the function provided by Google NLP:https://cloud.google.com/natural-language/docs/analyzing-sentiment.
```python
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
```
So we input our json file to the analyzer, then . we got the sentiment analysis as follow.Sentiment is represented by numerical `score` and `magnitude` values. Score of the sentiment ranges between -1.0 (negative) and 1.0 (positive) and corresponds to the overall emotional leaning of the text. Magnitude indicates the overall strength of emotion (both positive and negative) within the given text, between 0.0 and +inf. In this case, the text has a slight positive emotion according to the value of `Score` and `Magnitude`. 

User Name: veraq7239
Content: @foston_q Boston is such a lovely city but the green line is just getting so busy during the peak time everyday ! Ahttps://t.co/3ipEDEQHJG
Score: 0.20000000298023224
Magnitude: 0.4000000059604645

## Get text sorted
Then we sort the text by score in ascending order. If the scores are same, then sort by maginitude.
```python
# Sort the complians according to the sentiment score
df = df.sort_values(by=['Score','Magnitude'])
df = df.reset_index().drop('index',axis = 1)
```
Here's the result.
![result](https://github.com/qinghan531/ec601TWHK/blob/work_qing/dataframe.png)

## Identify department
At the same time, we could figure out the main problem each grievance mentioned, which department they belongs to. We currently set up four departments: Safety, Cleaness, Peak Hour and General. So we build a department dictionary whcih contains much of the adjective words related to each department. And then compare each sentences with words in dictionary to figure out which department it belongs to. The result after department identification is shown below.
![result](https://github.com/qinghan531/ec601TWHK/blob/work_qing/department%20identification.png)

## Send email to relevant department
After the sentiment analysis, we send the most negative grievance to relevant. For our project, we set up an email address to recieve the information. Here's the code for the sendemail function.
```python
import smtplib, ssl
# coding=utf-8
def sendemail(sender, receiver, username, content, department):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = sender  # Enter your address
    receiver_email = receiver  # Enter receiver address
    password = input("Type your password and press enter: ")
    message = """\
    Subject: Gravience from twitter

    """ + "To " + department + " Department:" + "\n" + content + "\n" + "From " + username

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
 ```
 Finally, we recieved the email of the tweet that reflects some problem in Boston transportation.  
 ![result](https://github.com/qinghan531/ec601TWHK/tree/work_qing)
 
---
To set up the twitter API, view this link:
http://socialmedia-class.org/twittertutorial.html

To get started with Google Natural Language API, view this link:
https://cloud.google.com/natural-language/docs/
