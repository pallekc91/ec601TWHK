import sys
import six
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import datetime
import json

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
    return_json = {}
    for entity in result.entities:
        for mention in entity.mentions:
            return_json["Begin Offset"] = format(mention.text.begin_offset)
            return_json["Content"] = format(mention.text.content)
            return_json["Magnitude"] = format(mention.sentiment.magnitude)
            return_json["Score"] = format(mention.sentiment.score)
            return_json["Type"] = format(mention.type)
            return_json["Salience"] = format(entity.salience)
    return return_json

def analysis_json(input_twitter_json):
    for key in input_twitter_json.keys():
        input_twitter_json[key]['google_score'] = analysis(input_twitter_json[key]['text'])
    name = ('JsonFromSentimentAnanlysis'+str(datetime.datetime.now())+'.json').replace(" ","");
    twitterJsonFile = open(name,"w");
    twitterJsonFile.write(json.dumps(input_twitter_json, indent=4))
