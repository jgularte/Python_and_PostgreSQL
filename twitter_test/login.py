from utility import twitter
import oauth2
import urllib.parse as urlparse

consumer = oauth2.Consumer(twitter.CONSUMER_KEY, twitter.CONSUMER_SECRET)
client = oauth2.Client(consumer)

response, content = client.request(twitter.REQUEST_TOKEN_URL, 'POST')

if response.status != 200:
    print('An error occurred!')

request_token = dict(urlparse.parse_qsl(content.decode("utf-8")))
