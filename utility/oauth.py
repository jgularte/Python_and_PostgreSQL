import oauth2
from utility import twitter
import urllib.parse as urlparse

# todo: make consumer not a global variable within the file. Maybe its own class?
consumer = oauth2.Consumer(twitter.CONSUMER_KEY, twitter.CONSUMER_SECRET)


def get_request_token():
    client = oauth2.Client(consumer)
    response, content = client.request(twitter.REQUEST_TOKEN_URL, 'POST')

    if response.status != 200:
        print('An error occurred getting the request token. Exiting...')
        exit(1)

    # Get request token
    return dict(urlparse.parse_qsl(content.decode("utf-8")))


def get_oauth_verifier(request_token):
    print("Go to the following website in your browser:")
    print(get_oauth_verifier_url(request_token))

    return input("what is the PIN? ")


def get_oauth_verifier_url(request_token):
    return "{0}?oauth_token={1}".format(twitter.AUTHORIZATION_URL, request_token['oauth_token'])


def get_access_token(request_token, oauth_verifier):
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    client = oauth2.Client(consumer, token)
    response, content = client.request(twitter.ACCESS_TOKEN_URL, 'POST')
    return dict(urlparse.parse_qsl(content.decode('UTF-8')))
