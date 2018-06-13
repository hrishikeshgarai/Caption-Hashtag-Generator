


#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys  
import json
from datetime import datetime  
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

#Variables that contains the user credentials to access Twitter API 
access_token = "919581457982640128-ullOyY52aA057rB3bBp0P0j7xBrEJFg"
access_token_secret = "7qnHxbaEE3NnG5XwAxC1IKGBZnPcuAWIWG6Gpl7LiOdpQ"
consumer_key = "ZSh6PfXZzVZl2iSrwpMXeiNkW"
consumer_secret = "sc7RXbO7LXocrdnuWfaube6VinvWx6HWKc0IxTvyEoLMnCf2xZ"
aws_access_key_id = 'AKIAJCVRO2SBCBGZ4O6Q'
aws_secret_access_key = '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'

host = 'search-hashtags-3cldgb3rsjhlmjztjrwnbd2n5a.us-east-2.es.amazonaws.com'
awsauth = AWS4Auth(aws_access_key_id,aws_secret_access_key,'us-east-2', 'es')

es = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        json_data = json.loads(data)
        if 'text' in json_data:
            for hashtag in json_data['entities']['hashtags']:
                if hashtag['text'] and json_data['user']['lang']=="en":
                    tags=hashtag['text']
                    try:
                        es.index(index="id1", doc_type="hash", body={"hash": tags})
                        print tags
                    except Exception:
                        pass
        
    def on_error(self, status):
        print status        

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
   
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    # es.index(index="id1", doc_type="hash", body={"hashtag": "tag"})
    # es.indices.delete(index="id1", ignore=[400, 404])

    try:
        l = StdOutListener()
        stream = Stream(auth, l)
        stream.filter(locations=[-180,-90,180,90])
    except Exception as e:
        raise e
