from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from config import CONSUMER_KEY, CONSUMER_SECRET
from config import ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from info import data
import geocoder
# OAuth process
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


# listener that handles streaming data
class listener(StreamListener):
    def on_connect(self):
        print('Stream starting...')

    def on_status(self, status):
         if status['user']['location'] != 'Nairobi':
            if status.geo is None:
                status.geo = geocoder.google(status['user']['location'])
                t = dict()
                t['text'] = status.text
                t['coordinates'] = geocoder.google(status['user']['location'])
                data.append(t)

            elif status.geo is not None:
                t = dict()
                t['text'] = status.text
                t['coordinates'] = status.coordinates
                data.append(t)

    def on_error(self, status):
        print(status)


def main():
    twitterStream = Stream(auth, listener())
    twitterStream.filter(locations=[
        -130.78125, -31.3536369415, 140.625, 63.8600358954
    ])
